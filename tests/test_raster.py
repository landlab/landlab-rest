import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_almost_equal, assert_array_equal


@pytest.mark.parametrize("graph_type", ("hex", "radial", "raster"))
def test_graph_status(client, graph_type):
    response = client.get("/graphs/{0}".format(graph_type))
    assert response.status_code == 200

    data = response.get_json()
    assert data["_type"] == "graph"
    assert "graph" in data


@pytest.mark.parametrize("graph_type", ("hex", "radial", "raster"))
def test_graph_data(client, graph_type):
    graph = xr.Dataset.from_dict(
        client.get("/graphs/{0}".format(graph_type)).get_json()["graph"]
    )

    assert set(graph.dims) == {
        "cell",
        "corner",
        "face",
        "link",
        "max_cell_faces",
        "max_patch_links",
        "node",
        "patch",
        "Two",
    }
    assert set(graph.variables) == {
        "corner",
        "corners_at_face",
        "dual",
        "faces_at_cell",
        "links_at_patch",
        "mesh",
        "node",
        "node_at_cell",
        "nodes_at_face",
        "nodes_at_link",
        "x_of_corner",
        "x_of_node",
        "y_of_corner",
        "y_of_node",
    }


def test_raster_default(client):
    graph = xr.Dataset.from_dict(client.get("/graphs/raster").get_json()["graph"])

    assert graph.dims == {
        "cell": 1,
        "corner": 4,
        "face": 4,
        "link": 12,
        "node": 9,
        "patch": 4,
        "max_cell_faces": 4,
        "max_patch_links": 4,
        "Two": 2,
    }

    assert_array_equal(
        graph.nodes_at_link,
        [
            [0, 1],
            [1, 2],
            [0, 3],
            [1, 4],
            [2, 5],
            [3, 4],
            [4, 5],
            [3, 6],
            [4, 7],
            [5, 8],
            [6, 7],
            [7, 8],
        ],
    )
    assert_array_equal(graph.x_of_node, [0.0, 1.0, 2.0, 0.0, 1.0, 2.0, 0.0, 1.0, 2.0])
    assert_array_equal(graph.y_of_node, [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0])
    assert_array_equal(graph.x_of_corner, [0.5, 1.5, 0.5, 1.5])
    assert_array_equal(graph.y_of_corner, [0.5, 0.5, 1.5, 1.5])
    assert_array_equal(
        graph.links_at_patch, [[3, 5, 2, 0], [4, 6, 3, 1], [8, 10, 7, 5], [9, 11, 8, 6]]
    )
    assert_array_equal(graph.corners_at_face, [[0, 1], [0, 2], [1, 3], [2, 3]])


def test_raster_default_shape(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/raster").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/raster?shape=3,3").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_raster_default_spacing(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/raster").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/raster?spacing=1").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


def test_raster_default_origin(client):
    graph_1 = xr.Dataset.from_dict(client.get("/graphs/raster").get_json()["graph"])
    graph_2 = xr.Dataset.from_dict(
        client.get("/graphs/raster?origin=0.0,0.0").get_json()["graph"]
    )

    assert_array_almost_equal(graph_1.x_of_node, graph_2.x_of_node)
    assert_array_almost_equal(graph_1.y_of_node, graph_2.y_of_node)


@pytest.mark.parametrize("n_cols", (4, 8, 16, 32))
@pytest.mark.parametrize("n_rows", (4, 8, 16, 32))
def test_raster_shape(client, n_rows, n_cols):
    url = "/graphs/raster?shape={0},{1}".format(n_rows, n_cols)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])
    assert graph.dims["node"] == n_rows * n_cols


@pytest.mark.parametrize("dy", (1.0, 2.0, 4.0))
@pytest.mark.parametrize("dx", (1.0, 2.0, 4.0))
def test_raster_spacing(client, dx, dy):
    url = "/graphs/raster?spacing={0},{1}".format(dy, dx)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])

    expected_x, expected_y = np.meshgrid([0.0, 1.0, 2.0], [0.0, 1.0, 2.0])

    assert_array_almost_equal(graph.x_of_node, expected_x.reshape((-1,)) * dx)
    assert_array_almost_equal(graph.y_of_node, expected_y.reshape((-1,)) * dy)


@pytest.mark.parametrize("y0", (-1.0, 1.0, 2.0, 4.0))
@pytest.mark.parametrize("x0", (-1.0, 1.0, 2.0, 4.0))
def test_raster_origin(client, x0, y0):
    url = "/graphs/raster?origin={0},{1}".format(y0, x0)
    graph = xr.Dataset.from_dict(client.get(url).get_json()["graph"])

    expected_x, expected_y = np.meshgrid([0.0, 1.0, 2.0], [0.0, 1.0, 2.0])

    assert_array_almost_equal(graph.x_of_node, expected_x.reshape((-1,)) + x0)
    assert_array_almost_equal(graph.y_of_node, expected_y.reshape((-1,)) + y0)
