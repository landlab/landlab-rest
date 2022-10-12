===================
Starting the server
===================

Use the ``start-sketchbook`` command to start running a *landlab-rest* server,

.. code::

    start-sketchbook

Look at the line containing `Serving on` to see what host and port the
server is running on. Alternatively, you can use the `--host` and `--port`
options to specify a specific host and port (``--help`` for help).

Once running, you should now be able to send requests to the server. For instance,
to get a `RasterModelGrid`,

.. code::

    curl https://0.0.0.0:8080/graphs/raster
