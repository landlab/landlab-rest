import urllib

import pytest


@pytest.mark.parametrize("graph_type", ("hex", "radial", "raster"))
def test_response_status(client, graph_type):
    response = client.get("/graphs/{0}".format(graph_type))
    assert response.status_code == 200


@pytest.mark.parametrize("graph_type", ("hex", "radial", "raster"))
def test_response_type(client, graph_type):
    response = client.get("/graphs/{0}".format(graph_type))
    data = response.get_json()
    assert data["_type"] == "graph"
    assert "graph" in data


@pytest.mark.parametrize("graph_type", ("hex", "radial", "raster"))
def test_response_href(client, graph_type):
    response = client.get("/graphs/{0}".format(graph_type))
    data = response.get_json()

    parts = urllib.parse.urlsplit(data["href"])
    assert parts[0] == ""
    assert parts[1] == ""
    assert parts[2] == "/graphs/{0}".format(graph_type)
    assert urllib.parse.parse_qs(parts[3])
    assert parts[4] == ""


@pytest.mark.parametrize(
    "graph_type,expected",
    (
        ("hex", "DualHexGraph"),
        ("radial", "DualRadialGraph"),
        ("raster", "DualUniformRectilinearGraph"),
    ),
)
def test_response_repr(client, graph_type, expected):
    response = client.get("/graphs/{0}".format(graph_type))
    data = response.get_json()

    assert data["repr"].startswith(expected)
