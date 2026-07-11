What is Nexus Gateway?
======================

Nexus Gateway is an open-source API gateway designed for teams running 
microservice architectures. It acts as a single entry point for all client 
requests, handling cross-cutting concerns such as authentication, rate limiting, 
and request routing before traffic reaches your backend services.

.. figure:: /_static/architecture.png
   :alt: Nexus Gateway architecture diagram
   :align: center

   *The Nexus Gateway sits between clients and your backend services.*

Core Responsibilities
---------------------

An API gateway is responsible for tasks that would otherwise need to be 
implemented individually in every service. Nexus Gateway centralises these 
concerns so your services can focus on business logic.

The main responsibilities of Nexus Gateway are:

- **Traffic routing** — directing incoming requests to the correct backend 
  service based on path, headers, or other request attributes.
- **Authentication and authorisation** — verifying the identity of clients 
  and enforcing access policies before requests reach your services.
- **Rate limiting** — protecting backend services from traffic spikes and 
  abuse by controlling how many requests a client can make over a given period.
- **Request and response transformation** — modifying headers, query 
  parameters, or payloads in transit when needed.
- **Observability** — collecting metrics, logs, and traces across all 
  incoming traffic from a single point.

How Nexus Gateway Fits Into Your Architecture
---------------------------------------------

In a typical deployment, Nexus Gateway runs at the edge of your infrastructure, 
directly behind your load balancer or ingress controller. All external traffic 
passes through the gateway before reaching any internal service.

This placement gives you a consistent enforcement layer for security and 
operational policies without modifying individual services.

Nexus Gateway is stateless by design. Configuration is defined in a YAML 
file or via the Admin API, and the gateway reads this configuration at 
startup or when a reload is triggered.

When to Use Nexus Gateway
--------------------------

Nexus Gateway is a good fit if your team:

- Runs three or more backend services that share authentication requirements.
- Needs fine-grained rate limiting per client, endpoint, or plan tier.
- Wants a single place to manage routing rules without modifying service code.
- Requires audit logs of all API traffic for compliance purposes.

If you are running a single service with straightforward access requirements, 
a dedicated gateway may introduce unnecessary complexity. A simple reverse 
proxy may be sufficient in that case.

.. note::
   Nexus Gateway is not a service mesh. It handles north-south traffic 
   (client to service), not east-west traffic (service to service). For 
   east-west communication patterns, consider a service mesh such as Istio 
   or Linkerd alongside Nexus Gateway.
