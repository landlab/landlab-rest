.. image:: https://github.com/landlab/landlab-rest/actions/workflows/test.yml/badge.svg
    :target: https://github.com/landlab/landlab-rest/actions/workflows/test.yml

.. image:: https://github.com/landlab/landlab-rest/actions/workflows/flake8.yml/badge.svg
    :target: https://github.com/landlab/landlab-rest/actions/workflows/flake8.yml

.. image:: https://github.com/landlab/landlab-rest/actions/workflows/black.yml/badge.svg
    :target: https://github.com/landlab/landlab-rest/actions/workflows/black.yml

landlab REST
============

A RESTful interface to landlab graphs.

Quickstart
----------

.. start-quickstart

To get started you will need to install the *landlab-rest* package, which is currently distributed
on `PyPI`_.

1.  Install *landlab-rest* into your current environment.

    .. code:: bash
    
        pip install landlab-rest

2.  Start the server.

    .. code:: bash
    
        start-sketchbook

3.  You can now send queries to the *landlab-rest* service.

    .. code:: bash

        curl https://0.0.0.0:8080/graphs/

.. _PyPI: https://pypi.org/project/landlab-rest/

.. end-quickstart

.. start-running

Start the server,

.. code::

    start-sketchbook

Look at the line containing `Serving on` to see what host and port the
server is running on. Alternatively, you can use the `--host` and `--port`
options to specify a specific host and port (`--help` for help).

Now you should be able to send requests to the server. For instance,
to get a `RasterModelGrid`,

.. code::

    curl https://0.0.0.0:8080/graphs/raster

For a list of supported graphs

.. code::

    curl https://0.0.0.0:8080/graphs/

You can pass parameters like,

.. code::

    curl 'https://0.0.0.0:8080/graphs/raster?shape=4,5&spacing=2.,1.'


Docker
------

To build a new docker image that will be a landlab-rest server,

.. code::

    docker build . -t landlab-rest


After building, run the server,

.. code::

    docker run -it -p 80:80 landlab-rest

Once running, you can then send requests to the server. For example,

.. code::

    curl https://0.0.0.0/graphs/raster

.. end-running
