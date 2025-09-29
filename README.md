# Burp Suite Extension: GraphQL sha256Hash Auto-Updater

This Burp Suite extension automatically recalculates and updates the `sha256Hash` parameter in GraphQL API requests whenever the `query` field is modified. It’s designed for APIs that use persisted queries (like Apollo Persisted Queries) and require a SHA-256 hash of the full query string.

---

## 🚀 Key Features

- **Automatic hash update:** Instantly recalculates the `sha256Hash` when you edit/tamper with a query in Burp Suite.
- **Works across Burp tools:** Supports Proxy, Repeater, and Scanner.
- **No manual work:** Just modify the query—hashing happens behind the scenes.
- **Domain filtering:** Only activates for specified target hosts.
- **Verbose logging:** Prints old/new hash and the query in the Burp Extender Output tab for full transparency.

---

## 🧠 How It Works

1. **Intercepts HTTP requests** with content-type `application/json`.
2. **Checks for `query` and `sha256Hash` fields** in the JSON body.
3. **Calculates the SHA-256 hash** of the exact `query` string (whitespace-sensitive).
4. **Updates the `sha256Hash`** field if the query changed.
5. **Logs all changes** (including hashes and query) to the Output tab.

---

## 🔒 Why Use This Extension?

Modern GraphQL APIs often reject requests if the `sha256Hash` doesn't exactly match the query. This extension automates the process, so you can freely test, tamper, and replay queries without manually recalculating the hash each time.
