Request Routing
===============

Routing is the process of matching an incoming request to a backend service 
and forwarding it. In Nexus Gateway, routing rules are defined as a list of 
routes in the configuration file. The gateway evaluates routes in order and 
forwards the request to the first matching route.

Route Matching
---------------

Each route defines one or more match conditions. A request must satisfy all 
conditions on a route to be considered a match.

**Path matching** is the most common condition. Nexus Gateway supports three 
path match types:

- **Exact** — the request path must match the configured path exactly.
- **Prefix** — the request path must begin with the configured prefix.
- **Regex** — the request path must match a regular expression.

In addition to path matching, routes can match on:

- **HTTP method** — restrict a route to specific methods such as ``GET`` or 
  ``POST``.
- **Headers** — match on the presence or value of a request header.
- **Query parameters** — match on the presence or value of a query parameter.

Route Priority
---------------

Routes are evaluated in the order they appear in the configuration file. 
The first route that matches the incoming request is used. Subsequent routes 
are not evaluated.

This means more specific routes should be defined before broader ones. For 
example, a route matching ``/api/v1/users/admin`` exactly should appear 
before a route matching the ``/api/v1/users`` prefix.

.. code-block:: yaml

   routes:
     - path: /api/v1/users/admin
       match_type: exact
       upstream: admin-service:8080

     - path: /api/v1/users
       match_type: prefix
       upstream: users-service:8080

If these routes were reversed, requests to ``/api/v1/users/admin`` would 
be matched by the prefix route first and routed to the wrong upstream.

Upstream Configuration
-----------------------

Each route must specify an upstream — the backend service address to which 
matching requests are forwarded.

Nexus Gateway supports three upstream formats:

- **Host and port** — ``orders-service:8080`` — for services reachable by 
  hostname within the same network.
- **IP address and port** — ``10.0.1.15:3000`` — for services referenced 
  by IP.
- **URL** — ``https://api.partner.example.com`` — for external upstreams 
  or when TLS is required on the upstream connection.

Load Balancing
---------------

When a route's upstream resolves to multiple instances — for example, via 
DNS round-robin or a service registry integration — Nexus Gateway distributes 
traffic across them using a configurable load balancing strategy.

The available strategies are:

- **Round robin** (default) — requests are distributed evenly across all 
  healthy instances in rotation.
- **Least connections** — each new request is sent to the instance with the 
  fewest active connections.
- **IP hash** — the client IP address is hashed to select an instance, 
  ensuring that requests from the same client consistently reach the same 
  upstream. Useful for stateful applications.

Health Checks
--------------

Nexus Gateway performs periodic health checks against upstream instances. 
Instances that fail a health check are removed from the routing pool until 
they recover.

Health checks are configured per upstream and support both HTTP and TCP 
probe types.

.. note::
   If all instances of an upstream fail their health checks simultaneously, 
   Nexus Gateway returns a ``503 Service Unavailable`` response to clients 
   until at least one instance recovers.
