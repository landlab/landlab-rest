================
Sending requests
================

For a list of supported graphs

.. code:: bash

    curl https://0.0.0.0:8080/graphs/

A uniform rectilinear graph (i.e. a raster),

.. code:: bash

    curl https://0.0.0.0:8080/graphs/raster

You can pass parameters like,

.. code:: bash

    curl 'https://0.0.0.0:8080/graphs/raster?shape=4,5&spacing=2.,1.'

----------
Graphs API
----------


GET /graphs
===========

List graphs.

:Description: List the names of all the supported *Landlab* graphs.
:Status Codes:
    * 200 OK – An array of strings.
:Examples:
    
    .. code-block:: bash
    
       curl 'https://0.0.0.0:8080/graphs/'

GET /graphs/{name}
==================

Get the graph structure.

:Description: Get the *x* and *y* positions of the elements of a graph along
    with their connectivity.
:Parameters:
    * name (string) - A name of a *Landlab* graph.
:Query Parameters:
    * shape (string) - The number of rows and columns
    * spacing (string) - The spacing between columns and rows
    * origin (string) - The *x* and *y* position of the lower-left of the grid
:Status Codes:
    * 200 OK – A Graph object.
:Examples:

    .. code-block:: bash
    
       curl 'https://0.0.0.0:8080/graphs/raster'
    
    A raster grid with 4 rows and 5 columns or nodes with a columns spacing of 2.0
    and a row spacing of 1.0.
    
    .. code-block:: bash
    
       curl 'https://0.0.0.0:8080/graphs/raster?shape=4,5&spacing=2.,1.'
    
    