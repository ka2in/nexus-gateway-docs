Getting Started
===============

This guide walks you through installing Nexus Gateway, writing your first 
configuration file, and routing a request to a backend service. By the end, 
you will have a working gateway instance running locally.

Prerequisites
-------------

Before you begin, make sure you have the following:

- A machine running Linux, macOS, or Windows with WSL2.
- Docker installed and running, or a Go toolchain (version 1.21 or later) 
  if you prefer to build from source.
- A terminal and basic familiarity with YAML files.

You do not need any existing infrastructure. The getting started guide uses 
a local mock service as the upstream target.

Step 1 — Download Nexus Gateway
---------------------------------

Pull the official Docker image:

.. code-block:: bash

   docker pull nexustech/gateway:2.4

Verify the image is available:

.. code-block:: bash

   docker images nexustech/gateway

You should see the ``2.4`` tag listed in the output.

Step 2 — Create a Configuration File
--------------------------------------

Create a file named ``nexus.yaml`` in your working directory with the 
following content:

.. code-block:: yaml

   gateway:
     port: 8080
     admin_port: 9000

   routes:
     - name: hello-route
       path: /hello
       match_type: prefix
       upstream: httpbin.org:80

This configuration starts the gateway on port ``8080`` and routes all 
requests to ``/hello`` to the public ``httpbin.org`` service, which we 
use here as a convenient upstream for testing.

Step 3 — Start the Gateway
----------------------------

Run the gateway with your configuration file:

.. code-block:: bash

   docker run --rm \
     -p 8080:8080 \
     -p 9000:9000 \
     -v $(pwd)/nexus.yaml:/etc/nexus/nexus.yaml \
     nexustech/gateway:2.4

You should see startup logs indicating the gateway has loaded your 
configuration and is listening on port ``8080``.

Step 4 — Send a Test Request
------------------------------

In a new terminal window, send a request through the gateway:

.. code-block:: bash

   curl http://localhost:8080/hello/get

The gateway receives your request, matches it to ``hello-route``, and 
forwards it to ``httpbin.org``. The response from ``httpbin.org`` is 
returned to your terminal.

If you see a JSON response from httpbin, your gateway is working correctly.

Step 5 — Check the Admin API
------------------------------

Nexus Gateway exposes an Admin API on the configured ``admin_port``. Use 
it to inspect the current configuration and route status:

.. code-block:: bash

   curl http://localhost:9000/api/routes

The response lists all configured routes and their current status. 
This endpoint is useful for verifying that configuration changes have 
been applied correctly.

Next Steps
-----------

Now that you have a running gateway, explore the following topics to 
continue building your configuration:

- :doc:`configuring-routes` — learn how to define routes for your 
  own services, add authentication, and apply rate limits.
- :doc:`../concepts/authentication` — understand the authentication 
  methods Nexus Gateway supports.
- :doc:`../concepts/rate-limiting` — configure rate limits to protect 
  your backend services.
