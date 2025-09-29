# -*- coding: utf-8 -*-
#Author: Jasveer Singh

from burp import IBurpExtender, IHttpListener
import json
import hashlib

EXT_NAME = "GraphQL sha256Hash Auto-Updater"
TARGET_HOST = "domain.com"
MAX_QUERY_LEN = 800  # For logging

def _maybe_truncate(s, limit=MAX_QUERY_LEN):
    if not isinstance(s, basestring):
        s = repr(s)
    return (s[:limit] + "\n...<truncated>..." if len(s) > limit else s)

class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName(EXT_NAME)
        callbacks.registerHttpListener(self)
        print("Extension Loaded Successfully")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            return
        request = messageInfo.getRequest()
        analyzedRequest = self._helpers.analyzeRequest(request)
        headers = analyzedRequest.getHeaders()

        # Domain filter
        host_header = None
        for h in headers:
            if h.lower().startswith("host:"):
                host_header = h.split(":", 1)[1].strip()
                break
        if not host_header or host_header.lower() != TARGET_HOST.lower():
            return

        # Only handle JSON content-type
        content_type = None
        for h in headers:
            if h.lower().startswith("content-type:"):
                content_type = h.lower()
        if not (content_type and "application/json" in content_type):
            return

        # Get body as string
        body_bytes = request[analyzedRequest.getBodyOffset():]
        try:
            body = "".join([chr(b & 0xFF) for b in body_bytes])
            j = json.loads(body)
        except Exception as e:
            return

        try:
            query = j["query"]
            hash_obj = j["extensions"]["persistedQuery"]
            old_hash = hash_obj.get("sha256Hash", None)
            if old_hash is not None:
                new_hash = hashlib.sha256(query.encode('utf-8')).hexdigest()
                if old_hash != new_hash:
                    # Logging: before updating hash
                    print("=== GraphQL sha256Hash update ===")
                    #print("Host: %s" % host_header)
                    try:
                        url = self._helpers.analyzeRequest(messageInfo).getUrl()
                        print("URL: %s" % str(url))
                    except:
                        pass
                    print("Old hash (captured in request): %s" % old_hash)
                    print("New hash (recalculated for query): %s" % new_hash)
                    #print("--- Query (in request, used for new hash): ---")
                    #print(_maybe_truncate(query))
                    #print("=== End ===\n")

                    # Update the hash in request
                    hash_obj["sha256Hash"] = new_hash
                    new_body = json.dumps(j, separators=(',', ':'))
                    new_message = self._helpers.buildHttpMessage(headers, new_body)
                    messageInfo.setRequest(new_message)
        except Exception as e:
            return
