import urllib
import json

from flask import Blueprint, jsonify, request, Response
import xarray as xr
import numpy as np

from landlab.graph import (DualUniformRectilinearGraph, DualHexGraph,
                           DualRadialGraph)


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


def to_resource(graph, href=None):
    return {
        '_type': 'graph',
        'href': href,
        'graph': graph_as_dict(graph),
    }


def graph_as_dict(graph):
    nodes_at_link = graph.nodes_at_link
    corners_at_face = graph.corners_at_face

    x_of_link = np.mean(graph.x_of_node[nodes_at_link], axis=1)
    y_of_link = np.mean(graph.y_of_node[nodes_at_link], axis=1)
    x_of_face = np.mean(graph.x_of_corner[corners_at_face], axis=1)
    y_of_face = np.mean(graph.y_of_corner[corners_at_face], axis=1)

    dataset = xr.Dataset({
        'y_of_node': xr.DataArray(graph.y_of_node, dims=('node', )),
        'x_of_node': xr.DataArray(graph.x_of_node, dims=('node', )),
        'y_of_corner': xr.DataArray(graph.y_of_corner, dims=('corner', )),
        'x_of_corner': xr.DataArray(graph.x_of_corner, dims=('corner', )),
        'y_of_link': xr.DataArray(y_of_link, dims=('link', )),
        'x_of_link': xr.DataArray(x_of_link, dims=('link', )),
        'y_of_face': xr.DataArray(y_of_face, dims=('face', )),
        'x_of_face': xr.DataArray(x_of_face, dims=('face', )),
        'nodes_at_link': xr.DataArray(nodes_at_link,
                                      dims=('link', 'nodes_per_link', )),
        'corners_at_face': xr.DataArray(corners_at_face,
                                      dims=('face', 'corners_per_face', )),
        'nodes_at_patch': xr.DataArray(graph.nodes_at_patch,
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

    graph = DualUniformRectilinearGraph(shape, spacing=spacing)

    return as_resource(to_resource(
        graph,
        href='/graph/raster?{params}'.format(params=urllib.urlencode(args))))


@graphs_page.route('/hex')
def hex():
    args = dict(shape=request.args.get('shape', '4,4'),
                spacing=request.args.get('spacing', '1.'),)

    shape = [int(n) for n in args['shape'].split(',')]
    spacing = float(args['spacing'])

    graph = DualHexGraph(shape, spacing=spacing, node_layout='hex')

    return as_resource(to_resource(
        graph,
        href='/graph/hex?{params}'.format(params=urllib.urlencode(args))))


@graphs_page.route('/radial')
def radial():
    args = dict(shape=request.args.get('shape', '4,6'),
                spacing=request.args.get('spacing', '1.'))
    # args = dict(shape=request.args.get('shape', '1,1'))

    shape = [int(n) for n in args['shape'].split(',')]
    spacing = float(args['spacing'])
    # n_shells, dr = shape[0], 2. * np.pi / shape[1]
    #n_shells, dr = shape[0], shape[1]

    graph = DualRadialGraph(shape=shape, spacing=spacing)
    # graph = DualRadialGraph(shape=(shape[0], 6), spacing=dr)

    return as_resource(to_resource(
        graph,
        href='/graph/radial?{params}'.format(params=urllib.urlencode(args))))
