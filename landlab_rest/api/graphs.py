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
    return grid.ds.to_dict()


@graphs_page.route("/")
def show():
    graphs = ["hex", "raster", "radial"]
    graphs.sort()
    return jsonify(graphs)


@graphs_page.route("/raster")
def raster():
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
        origin=request.args.get("origin", "0.0,0.0"),
        orientation=request.args.get("orientation", "horizontal"),
        node_layout=request.args.get("node_layout", "rect"),
    )

    shape = tuple(int(n) for n in args["shape"].split(","))
    spacing = float(args["spacing"])
    origin = tuple(float(n) for n in args["origin"].split(","))

    grid = landlab.graph.DualHexGraph(
        shape,
        spacing=spacing,
        origin=origin,
        orientation=args["orientation"],
        node_layout=args["node_layout"],
    )

    return as_resource(
        to_resource(
            grid,
            href=urllib.parse.urlunsplit(
                ("", "", "/graphs/hex", urllib.parse.urlencode(args), "")
            ),
            repr_="DualHexGraph({shape}, spacing={spacing}, origin={origin}, orientation={orientation}, node_layout={node_layout})".format(
                shape=repr(shape),
                spacing=repr(spacing),
                origin=repr(origin),
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
        origin=request.args.get("origin", "0.0,0.0"),
    )

    shape = tuple(int(n) for n in args["shape"].split(","))
    spacing = float(args["spacing"])
    origin = tuple(float(n) for n in args["origin"].split(","))

    grid = landlab.graph.DualRadialGraph(shape, spacing=spacing, origin=origin)

    return as_resource(
        to_resource(
            grid,
            href=urllib.parse.urlunsplit(
                ("", "", "/graphs/radial", urllib.parse.urlencode(args), "")
            ),
            repr_="DualRadialGraph({shape}, spacing={spacing}, origin={origin})".format(
                shape=repr(shape), spacing=repr(spacing), origin=repr(origin)
            ),
        )
    )
