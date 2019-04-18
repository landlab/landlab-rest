import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_almost_equal, assert_array_equal


def test_hex_default(client):
    graph = xr.Dataset.from_dict(client.get("/graphs/hex").get_json()["graph"])

    assert graph.dims == {
        "cell": 4,
        "corner": 16,
        "face": 19,
        "link": 33,
        "node": 16,
        "patch": 18,
        "max_cell_faces": 6,
        "max_patch_links": 3,
        "Two": 2,
    }


def test_hex_default_shape(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/hex").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/hex?shape=4,4").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_hex_default_spacing(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/hex").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/hex?spacing=1").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_hex_default_origin(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/hex").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/hex?origin=0.0,0.0").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


@pytest.mark.parametrize("y0", (-1.0, 1.0, 2.0, 4.0))
@pytest.mark.parametrize("x0", (-1.0, 1.0, 2.0, 4.0))
def test_hex_origin(client, x0, y0):
    url = "/graphs/hex?origin={0},{1}".format(y0, x0)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])
    centered = xr.Dataset.from_dict(
        client.get("/graphs/hex?origin=0.0,0.0").get_json()["graph"]
    )

    assert_array_almost_equal(graph.x_of_node, centered.x_of_node + x0)
    assert_array_almost_equal(graph.y_of_node, centered.y_of_node + y0)
