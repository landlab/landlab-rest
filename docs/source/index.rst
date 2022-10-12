============
landlab REST
============

A web service for creating *Landlab* graph structures. Send
requests to retrieve data (as json objects) that describe *Landlab*
model grids. This includes,

* *x* and *y* coordinates of a grid's nodes and corners
* connectivity the the various grid elements

Currently available grid types include :class:`~landlab.grid.raster.RasterModelGrid`,
:class:`~landlab.grid.hex.HexModelGrid` and :class:`~landlab.grid.radial.RadialModelGrid`.

.. toctree::
  :maxdepth: 1
  :hidden:

  quickstart
  starting
  requests

.. toctree::
  :caption: Development
  :maxdepth: 1
  :hidden:

  contributing/index
  changes
  Contributors <authors>
  License <license>
