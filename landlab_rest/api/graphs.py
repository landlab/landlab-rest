import json
import urllib

import landlab
from flask import Blueprint, Response, jsonify, request

graphs_page = Blueprint("graphs", __name__)


def as_resource(resp):
    return Response(
        json.dumps(resp, sort_keys=True, indent=2, separators=(",", ": ")),
        mimetype="application/x-resource+json; charset=utf-8",
    )


def as_collection(resp):
    return Response(
        json.dumps(resp, sort_keys=True, indent=2, separators=(",", ": ")),
        mimetype="application/x-collection+json; charset=utf-8",
    )


def jsonify_collection(items):
    collection = []
    for item in items:
        collection.append(item.to_resource())
    return Response(
        json.dumps(collection, sort_keys=True, indent=2, separators=(",", ": ")),
        mimetype="application/x-collection+json; charset=utf-8",
    )


def to_resource(grid, href=None, repr_=None):
    return {"_type": "graph", "href": href, "graph": grid_as_dict(grid), "repr": repr_}


def grid_as_dict(grid):
    grid.ds.update(
        {
            "corner": grid.corners.reshape(-1),
            "x_of_corner": (("corner",), grid.x_of_corner),
            "y_of_corner": (("corner",), grid.y_of_corner),
            "faces_at_cell": (("cell", "max_cell_faces"), grid.faces_at_cell),
            "corners_at_face": (("face", "Two"), grid.corners_at_face),
        }
    )
    return grid.ds.to_dict()


@graphs_page.route("/")
def show():
    """Show available graphs.
    ---
    definitions:
        GraphName:
            type: string
            enum: ['hex', 'raster', 'radial']
        GraphNames:
            type: array
            items:
                $ref: '#definitions/GraphName'
    responses:
        200:
            description: A list of all available Landlab graphs.
            schema:
              $ref: '#/definitions/GraphNames'
            examples:
              ['hex', 'raster', 'radial']
    """
    graphs = sorted(["hex", "raster", "radial"])
    return jsonify(graphs)


@graphs_page.route("/raster")
def raster():
    """A 2D RasterGraph.
    ---
    parameters:
        - name: shape
          in: query
          type: string
          required: false
          default: '3,3'
        - name: spacing
          in: query
          type: string
          required: false
          default: '1.0,1.0'
        - name: origin
          in: query
          type: string
          required: false
          default: '0.0,0.0'

    definitions:
        Graph:
            type: object
            properties:
                dims:
                    $ref: '#/definitions/Dimensions'
                coords:
                    $ref: '#/definitions/Coordinates'
                data_vars:
                    $ref: '#/definitions/DataVars'
        DimensionName:
            type: string
            enum: ['Two', 'cell', 'corner', 'face', 'link', 'node', 'patch', 'max_cell_faces', 'max_patch_links']
        DimensionNames:
            type: array
            items: ['Two', 'cell', 'corner', 'face', 'link', 'node', 'patch', 'max_cell_faces', 'max_patch_links']

        Dimensions:
            type: object
            properties:
                Two:
                    type: integer
                cell:
                    type: integer
                corner:
                    type: integer
                face:
                    type: integer
                link:
                    type: integer
                node:
                    type: integer
                patch:
                    type: integer
                max_cell_faces:
                    type: integer
                max_patch_links:
                    type: integer
        Coordinates:
            type: object
            properties:
                corner:
                    $ref: '#/definitions/IntegerData'
                node:
                    $ref: '#/definitions/IntegerData'
        DataVars:
            type: object
            properties:
                corners_at_face:
                    dims:
                        type: array

                    $ref: '#/definitions/IntegerData'
                faces_at_cell:
                    $ref: '#/definitions/IntegerData'
                links_at_patch:
                    $ref: '#/definitions/IntegerData'
                node_at_cell:
                    $ref: '#/definitions/IntegerData'
                nodes_at_face:
                    $ref: '#/definitions/IntegerData'
                nodes_at_link:
                    $ref: '#/definitions/IntegerData'
                x_of_corner:
                    $ref: '#/definitions/FloatData'
                x_of_node:
                    $ref: '#/definitions/FloatData'
                y_of_corner:
                    $ref: '#/definitions/FloatData'
                y_of_node:
                    dims: ["node"]
                    data:
                        type: array
                        items: float
        IntegerData:
            type: object
            properties:
                dims:
                    type: array
                    items:
                        $ref: '#/definitions/DimensionNames'
                data:
                    type: array
                    items: integer
        FloatData:
            type: object
            properties:
                dims:
                    type: array
                    items:
                        $ref: '#/definitions/DimensionNames'
                data:
                    type: array
                    items: float

    responses:
        200:
            description: A raster graph.
            schema:
                $ref: '#/definitions/Graph'
    """
    args = dict(
        shape=request.args.get("shape", "3,3"),
        spacing=request.args.get("spacing", "1.0,1.0"),
        origin=request.args.get("origin", "0.0,0.0"),
    )

    shape = tuple(int(n) for n in args["shape"].split(","))
    spacing = tuple(float(n) for n in args["spacing"].split(","))
    origin = tuple(float(n) for n in args["origin"].split(","))

    grid = landlab.graph.DualUniformRectilinearGraph(
        shape, spacing=spacing, origin=origin
    )
    return as_resource(
        to_resource(
            grid,
            href=urllib.parse.urlunsplit(
                ("", "", "/graphs/raster", urllib.parse.urlencode(args), "")
            ),
            repr_="DualUniformRectilinearGraph({shape}, spacing={spacing}, origin={origin})".format(
                shape=repr(shape), spacing=repr(spacing), origin=repr(origin)
            ),
        )
    )


@graphs_page.route("/hex")
def hex():
    args = dict(
        shape=request.args.get("shape", "4,4"),
        spacing=request.args.get("spacing", "1.0"),
        yx_of_origin=request.args.get("origin", "0.0,0.0"),
        orientation=request.args.get("orientation", "horizontal"),
        node_layout=request.args.get("node_layout", "rect"),
    )

    shape = tuple(int(n) for n in args["shape"].split(","))
    spacing = float(args["spacing"])
    yx_of_origin = tuple(float(n) for n in args["yx_of_origin"].split(","))
    xy_of_origin = yx_of_origin[1], yx_of_origin[0]

    grid = landlab.graph.DualHexGraph(
        shape,
        spacing=spacing,
        xy_of_lower_left=xy_of_origin,
        orientation=args["orientation"],
        node_layout=args["node_layout"],
        sort=True,
    )

    return as_resource(
        to_resource(
            grid,
            href=urllib.parse.urlunsplit(
                ("", "", "/graphs/hex", urllib.parse.urlencode(args), "")
            ),
            repr_="DualHexGraph({shape}, spacing={spacing}, xy_of_lower_left={xy_of_origin}, orientation={orientation}, node_layout={node_layout})".format(
                shape=repr(shape),
                spacing=repr(spacing),
                xy_of_origin=repr(xy_of_origin),
                orientation=repr(args["orientation"]),
                node_layout=repr(args["node_layout"]),
            ),
        )
    )


@graphs_page.route("/radial")
def radial():
    args = dict(
        shape=request.args.get("shape", "3,4"),
        spacing=request.args.get("spacing", "1.0"),
        yx_of_origin=request.args.get("origin", "0.0,0.0"),
    )

    shape = tuple(int(n) for n in args["shape"].split(","))
    spacing = float(args["spacing"])
    yx_of_origin = tuple(float(n) for n in args["yx_of_origin"].split(","))
    xy_of_origin = yx_of_origin[1], yx_of_origin[0]

    grid = landlab.graph.DualRadialGraph(
        shape, spacing=spacing, xy_of_center=xy_of_origin, sort=True
    )

    return as_resource(
        to_resource(
            grid,
            href=urllib.parse.urlunsplit(
                ("", "", "/graphs/radial", urllib.parse.urlencode(args), "")
            ),
            repr_=f"DualRadialGraph({shape!r}, spacing={spacing!r}, xy_of_center={xy_of_origin!r})",
        )
    )
