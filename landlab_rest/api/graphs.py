import urllib
import json

from flask import Blueprint, jsonify, request, Response
import xarray as xr
import numpy as np

import landlab
from landlab.graph import DualUniformRectilinearGraph


graphs_page = Blueprint('graphs', __name__)

def as_resource(resp):
    return Response(json.dumps(resp, sort_keys=True, indent=2,
                               separators=(',', ': ')),
                    mimetype='application/x-resource+json; charset=utf-8')


def as_collection(resp):
    return Response(json.dumps(resp, sort_keys=True, indent=2,
                               separators=(',', ': ')),
                    mimetype='application/x-collection+json; charset=utf-8')


def jsonify_collection(items):
    collection = []
    for item in items:
        collection.append(item.to_resource())
    return Response(json.dumps(collection, sort_keys=True, indent=2,
                               separators=(',', ': ')),
                    mimetype='application/x-collection+json; charset=utf-8')


def to_resource(grid, graph, href=None):
    return {
        '_type': 'graph',
        'href': href,
        'graph': grid_as_dict(grid, graph),
    }


def grid_as_dict(grid, graph):
    nodes_at_link = np.vstack((grid.node_at_link_tail,
                               grid.node_at_link_head)).T
    corners_at_face = np.vstack((graph.corner_at_face_tail,
                                 graph.corner_at_face_head)).T

    dataset = xr.Dataset({
        'y_of_node': xr.DataArray(grid.y_of_node, dims=('node', )),
        'x_of_node': xr.DataArray(grid.x_of_node, dims=('node', )),
        'y_of_corner': xr.DataArray(graph.y_of_corner, dims=('corner', )),
        'x_of_corner': xr.DataArray(graph.x_of_corner, dims=('corner', )),
        'y_of_link': xr.DataArray(grid.y_of_link, dims=('link', )),
        'x_of_link': xr.DataArray(grid.x_of_link, dims=('link', )),
        'y_of_face': xr.DataArray(grid.y_of_face, dims=('face', )),
        'x_of_face': xr.DataArray(grid.x_of_face, dims=('face', )),
        'nodes_at_link': xr.DataArray(nodes_at_link,
                                      dims=('link', 'nodes_per_link', )),
        'corners_at_face': xr.DataArray(corners_at_face,
                                      dims=('face', 'corners_per_face', )),
        'nodes_at_patch': xr.DataArray(grid.nodes_at_patch,
                                       dims=('patch', 'nodes_per_patch', )),
        'corners_at_cell': xr.DataArray(graph.corners_at_cell,
                                        dims=('cell', 'corners_per_cell', )),
    })

    return dataset.to_dict()

    # return as_resource(dataset.to_dict())
    # return jsonify(dataset.to_dict())


@graphs_page.route('/')
def show():
    graphs = ['hex', 'raster', 'radial']
    graphs.sort()
    return jsonify(graphs)


@graphs_page.route('/raster')
def raster():
    args = dict(shape=request.args.get('shape', '3,3'),
                spacing=request.args.get('spacing', '1.,1.'),)

    shape = [int(n) for n in args['shape'].split(',')]
    spacing = [float(n) for n in args['spacing'].split(',')]

    grid = landlab.RasterModelGrid(shape, spacing=spacing)
    graph = DualUniformRectilinearGraph(shape, spacing=spacing)
    return as_resource(to_resource(
        grid, graph,
        href='/graph/raster?{params}'.format(params=urllib.urlencode(args))))


@graphs_page.route('/hex')
def hex():
    args = dict(shape=request.args.get('shape', '4,4'),
                spacing=request.args.get('spacing', '1.'),)

    shape = [int(n) for n in args['shape'].split(',')]
    spacing = float(args['spacing'])

    grid = landlab.HexModelGrid(*shape, dx=spacing)

    return as_resource(to_resource(
        grid,
        href='/graph/hex?{params}'.format(params=urllib.urlencode(args))))


@graphs_page.route('/radial')
def radial():
    args = dict(shape=request.args.get('shape', '4,4'))

    shape = [int(n) for n in args['shape'].split(',')]
    n_shells, dr = shape[0], 2. * np.pi / shape[1]

    grid = landlab.RadialModelGrid(n_shells, dr)

    return as_resource(to_resource(
        grid,
        href='/graph/radial?{params}'.format(params=urllib.urlencode(args))))
