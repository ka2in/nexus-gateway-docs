Configuring Routes
==================

This guide explains how to define routes in Nexus Gateway for real-world 
service deployments. It covers path matching, authentication, rate limiting, 
and header manipulation in a single configuration workflow.

A Route for a Real Service
---------------------------

The following example shows a complete route definition for a production 
API endpoint. It combines path matching, JWT authentication, and rate 
limiting in a single route block:

.. code-block:: yaml

   routes:
     - name: orders-api
       path: /api/v1/orders
       match_type: prefix
       methods: [GET, POST]
       upstream: orders-service:8080
       auth:
         type: jwt
         jwks_uri: https://auth.example.com/.well-known/jwks.json
         claims:
           iss: https://auth.example.com
       rate_limit:
         requests: 200
         window: 60s
         identifier: jwt_claim
         claim: sub

Walk through each field:

- ``name`` — a unique identifier for the route, used in logs and the 
  Admin API.
- ``path`` — the path prefix to match against incoming requests.
- ``methods`` — restricts the route to the listed HTTP methods. Requests 
  using other methods receive a ``405 Method Not Allowed`` response.
- ``upstream`` — the backend service address.
- ``auth`` — the authentication configuration. Here we use JWT with a 
  JWKS endpoint.
- ``rate_limit`` — applies a sliding window limit of 200 requests per 
  minute, counted per unique ``sub`` claim in the JWT.

Manipulating Request Headers
-----------------------------

Nexus Gateway can add, remove, or rewrite headers before forwarding 
a request to the upstream service. This is useful for passing 
authentication context, adding tracing headers, or removing headers 
that should not reach backend services.

.. code-block:: yaml

   routes:
     - name: internal-api
       path: /internal
       match_type: prefix
       upstream: internal-service:3000
       request_headers:
         set:
           X-Gateway-Version: "2.4"
           X-Request-Source: nexus-gateway
         remove:
           - X-Forwarded-For
           - Cookie

The ``set`` block adds or overwrites headers. The ``remove`` block 
deletes headers from the forwarded request entirely.

Handling Multiple Upstreams for the Same Path
----------------------------------------------

Some deployments require traffic splitting — for example, routing a 
percentage of traffic to a canary deployment while the rest goes to 
the stable version.

Nexus Gateway supports weighted upstream groups for this pattern:

.. code-block:: yaml

   routes:
     - name: products-canary
       path: /api/v1/products
       match_type: prefix
       upstreams:
         - address: products-service-stable:8080
           weight: 90
         - address: products-service-canary:8080
           weight: 10

In this configuration, 90% of traffic goes to the stable deployment 
and 10% to the canary. Adjust the weights to gradually shift traffic 
as confidence in the canary grows.

.. note::
   Weights are relative, not percentages. A configuration with weights 
   of ``9`` and ``1`` produces the same distribution as ``90`` and ``10``.

Testing Routes Without Restarting
-----------------------------------

After making changes to ``nexus.yaml``, you can reload the configuration 
without restarting the gateway process by sending a reload signal to 
the Admin API:

.. code-block:: bash

   curl -X POST http://localhost:9000/api/reload

The gateway validates the new configuration before applying it. If 
validation fails — for example, due to a missing required field or 
an invalid upstream address — the gateway logs the error and continues 
running with the previous configuration. No traffic is disrupted.

This makes it safe to iterate on your configuration in production 
environments.
