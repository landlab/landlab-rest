import pytest
from landlab_rest import create_app

app = create_app()


@pytest.fixture
def client():
    with app.test_client() as c:
        yield c
