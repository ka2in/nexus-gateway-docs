Authentication
==============

Nexus Gateway supports multiple authentication mechanisms and can enforce 
them independently per route. Authentication is handled at the gateway level, 
so backend services receive only verified requests.

Supported Authentication Methods
----------------------------------

API Keys
~~~~~~~~

API key authentication is the simplest method supported by Nexus Gateway. 
Clients include a key in the request header, and the gateway validates it 
against a configured key store.

By default, the gateway reads the key from the ``X-API-Key`` header. This 
header name is configurable per route.

API keys are suitable for server-to-server integrations where the client 
environment is controlled and the key can be stored securely.

JWT Authentication
~~~~~~~~~~~~~~~~~~

Nexus Gateway can validate JSON Web Tokens issued by any compatible identity 
provider. The gateway verifies the token signature, expiry, and configurable 
claims before forwarding the request.

Supported signing algorithms are ``RS256``, ``RS384``, ``RS512``, ``ES256``, 
and ``HS256``. The public key or JWKS endpoint is configured in the route 
definition.

.. code-block:: yaml

   routes:
     - path: /api/v1/orders
       upstream: orders-service:8080
       auth:
         type: jwt
         jwks_uri: https://auth.example.com/.well-known/jwks.json
         claims:
           iss: https://auth.example.com
           aud: nexus-gateway

OAuth 2.0 Token Introspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For deployments using an external authorisation server, Nexus Gateway supports 
OAuth 2.0 token introspection. The gateway calls the introspection endpoint 
with the bearer token and grants or denies the request based on the response.

This method adds latency because each request requires a call to the 
authorisation server. Use response caching to reduce the impact on 
high-traffic routes.

How Authentication Failures Are Handled
----------------------------------------

When a request fails authentication, Nexus Gateway returns a ``401 
Unauthorized`` response. The response body contains a JSON error object 
with a machine-readable error code and a human-readable message.

.. code-block:: json

   {
     "error": "invalid_token",
     "message": "The provided token has expired.",
     "request_id": "req_01HZ7K4PQRST9V"
   }

The ``request_id`` field is included in all error responses and can be 
used to trace the request in the gateway logs.

.. warning::
   Do not expose detailed authentication error messages to end users in 
   production. Use the ``error`` code in your client application to display 
   appropriate user-facing messages, and log the full response server-side.

Combining Authentication with Authorisation
--------------------------------------------

Authentication confirms who the client is. Authorisation determines what 
the client is allowed to do. Nexus Gateway handles both.

After a successful authentication check, the gateway can evaluate 
authorisation policies based on token claims, API key metadata, or 
request attributes such as HTTP method and path.

Authorisation policies are defined separately from authentication 
configuration and can be reused across multiple routes.
