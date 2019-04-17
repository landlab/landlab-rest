import pytest

from landlab_rest import create_app

app = create_app()


@pytest.fixture(scope="module")
def client():
    with app.test_client() as c:
        yield c


def test_health(client):
    response = client.get("/graphs/raster")
    assert response.status_code == 200
