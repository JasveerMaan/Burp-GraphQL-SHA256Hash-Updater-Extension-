# Burp Suite Extension: GraphQL sha256Hash Auto-Updater

This Burp Suite extension automatically recalculates and updates the sha256Hash parameter in GraphQL API requests when the query is modified in Burp Suite. It is designed for APIs that use persisted queries (such as Apollo Persisted Queries) and require a SHA-256 hash of the query string for validation

🚀 Key Features

Automatic hash calculation: Seamlessly recalculates the sha256Hash whenever the query field is modified in the request.

Works across Burp tools: Supports Proxy, Repeater, and Scanner for full testing coverage.

No manual steps needed: Edit your query as needed—hashes are updated on the fly before each request is sent.

Domain filtering: Only operates for specified target hosts, ensuring minimal interference with unrelated traffic.

Verbose logging: Outputs original and updated hash values, and the associated query, to the Burp Extender Output tab for full transparency and debugging.

🧠 How It Works

Intercepts outgoing HTTP requests with content-type application/json.

Checks for the presence of both query and sha256Hash fields in the JSON body.

Calculates the SHA-256 hash of the exact query string (including whitespace/formatting).

Updates the sha256Hash field with the new value if the query was changed.

Logs details (old/new hash, query, etc.) to the Output tab.

🔒 Why Use This Extension?

Persisted queries in GraphQL APIs require the hash to match the exact query being sent. During security testing, you often need to tamper with queries, but recalculating hashes manually is tedious and error-prone. This extension ensures your modified requests are always correctly signed, allowing for efficient and thorough security assessments.
