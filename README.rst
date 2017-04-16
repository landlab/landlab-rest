============
landlab REST
============

A RESTful interface to landlab graphs.


----------
Quickstart
----------

Use `conda` to install the necessary requirements,

.. code::

    $ conda install --file=requirements.txt -c conda-forge -c landlab

Start the server,

.. code::

    $ python ./server.py

Look at the line containing `Serving on` to see what host and port the
server is running on. Alternatively, you can use the `--host` and `--port`
options to specify a specific host and port (`--help` for help).

Now you should be able to send requests to the server. For instance,
to get a `RasterModelGrid`,

.. code::

    $ curl https://0.0.0.0:8080/graphs/raster

For a list of supported graphs

.. code::

    $ curl https://0.0.0.0:8080/graphs/

You can pass parameters like,

.. code::

    $ curl 'https://0.0.0.0:8080/graphs/raster?shape=4,5&spacing=2.,1.'
