import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_equal, assert_array_almost_equal


def test_radial_default(client):
    graph = xr.Dataset.from_dict(client.get("/graphs/radial").get_json()["graph"])

    assert graph.dims == {
        "cell": 13,
        "corner": 36,
        "face": 48,
        "link": 60,
        "node": 25,
        "patch": 36,
        "max_cell_faces": 6,
        "max_patch_links": 3,
        "Two": 2,
    }


def test_radial_default_shape(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/radial").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/radial?shape=3,4").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_radial_default_spacing(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/radial").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/radial?spacing=1").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_radial_default_origin(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/radial").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/radial?origin=0.0,0.0").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


@pytest.mark.parametrize("spacing", (0.5, 1.0, 2.0, 4.0))
def test_radial_spacing(client, spacing):
    url = "/graphs/radial?spacing={0}".format(spacing)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])
    unit = xr.Dataset.from_dict(
        client.get("/graphs/radial?spacing=1.0").get_json()["graph"]
    )

    assert_array_almost_equal(
        np.sqrt(graph.x_of_node ** 2 + graph.y_of_node ** 2),
        np.sqrt(unit.x_of_node ** 2 + unit.y_of_node ** 2) * spacing,
        5,
    )


@pytest.mark.parametrize("y0", (-1.0, 1.0, 2.0, 4.0))
@pytest.mark.parametrize("x0", (-1.0, 1.0, 2.0, 4.0))
def test_radial_origin(client, x0, y0):
    url = "/graphs/radial?origin={0},{1}".format(y0, x0)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])
    centered = xr.Dataset.from_dict(
        client.get("/graphs/radial?origin=0.0,0.0").get_json()["graph"]
    )

    assert_array_almost_equal(graph.x_of_node, centered.x_of_node + x0)
    assert_array_almost_equal(graph.y_of_node, centered.y_of_node + y0)
