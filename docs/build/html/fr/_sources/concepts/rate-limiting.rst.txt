Rate Limiting
=============

Rate limiting controls how many requests a client can make to a route within 
a defined time window. Nexus Gateway enforces rate limits at the gateway 
level, before requests reach backend services.

Why Rate Limiting Matters
--------------------------

Without rate limiting, a single misbehaving client — whether due to a bug, 
misconfiguration, or deliberate abuse — can consume enough resources to 
degrade service for all other clients.

Rate limiting protects your infrastructure by:

- Preventing individual clients from overwhelming backend services.
- Reducing the impact of denial-of-service attacks.
- Enforcing usage quotas for clients on different pricing tiers.
- Smoothing out traffic spikes caused by batch jobs or retry storms.

How Nexus Gateway Counts Requests
-----------------------------------

Nexus Gateway uses a **sliding window** algorithm by default. The window 
moves continuously rather than resetting at fixed intervals, which prevents 
bursts of traffic at window boundaries.

A fixed window option is also available for use cases where predictable 
reset times are required, such as billing-cycle quota enforcement.

Rate Limit Identifiers
-----------------------

Rate limits are applied per identifier. The identifier determines how the 
gateway groups requests for counting purposes. Supported identifiers are:

- **IP address** — limits requests from a single IP. Useful as a baseline 
  protection layer.
- **API key** — limits requests per authenticated client. The most common 
  approach for API products.
- **JWT claim** — limits requests based on a value from the token payload, 
  such as a ``sub`` or ``org_id`` claim.
- **Header value** — limits requests based on any request header. Useful 
  for custom client identification schemes.

Identifiers can be combined. For example, you can apply both a per-IP limit 
and a per-API-key limit to the same route. Both limits are enforced 
independently.

Rate Limit Response Headers
-----------------------------

When rate limiting is active on a route, Nexus Gateway includes standard 
rate limit headers in every response so clients can track their usage:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Header
     - Description
   * - ``X-RateLimit-Limit``
     - The maximum number of requests allowed in the window.
   * - ``X-RateLimit-Remaining``
     - The number of requests remaining in the current window.
   * - ``X-RateLimit-Reset``
     - The Unix timestamp when the window resets.
   * - ``Retry-After``
     - Seconds to wait before retrying. Present only on ``429`` responses.

When a client exceeds the limit, the gateway returns a ``429 Too Many 
Requests`` response and stops forwarding the request to the upstream service.

Configuring Rate Limits
------------------------

Rate limits are defined in the route configuration. The following example 
applies a limit of 100 requests per minute per API key:

.. code-block:: yaml

   routes:
     - path: /api/v1/products
       upstream: products-service:8080
       rate_limit:
         requests: 100
         window: 60s
         identifier: api_key

.. tip::
   Start with generous limits and tighten them based on observed traffic 
   patterns. Setting limits too low before understanding your clients' 
   request patterns leads to unnecessary friction.
