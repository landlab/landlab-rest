import json

import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_equal

from landlab_rest import create_app

app = create_app()


@pytest.fixture(scope="module")
def client():
    with app.test_client() as c:
        yield c


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
        "link",
        "node",
        "nodes_per_link",
        "nodes_per_patch",
        "patch",
    }
    assert set(graph.variables) == {
        "nodes_at_link",
        "x_of_node",
        "y_of_node",
        "nodes_at_patch",
        "nodes_at_link",
    }


def test_raster_default(client):
    graph = xr.Dataset.from_dict(client.get("/graphs/raster").get_json()["graph"])

    assert graph.dims == {
        "link": 12,
        "node": 9,
        "nodes_per_link": 2,
        "nodes_per_patch": 4,
        "patch": 4,
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
    assert_array_equal(
        graph.nodes_at_patch, [[4, 3, 0, 1], [5, 4, 1, 2], [7, 6, 3, 4], [8, 7, 4, 5]]
    )


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

    assert_array_equal(graph.x_of_node, expected_x.reshape((-1,)) * dx)
    assert_array_equal(graph.y_of_node, expected_y.reshape((-1,)) * dy)
