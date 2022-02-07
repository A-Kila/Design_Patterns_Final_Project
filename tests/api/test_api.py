import pytest
from fastapi.testclient import TestClient

from app.runner.setup import setup


@pytest.fixture()
def test_client() -> TestClient:
    app = setup()
    return TestClient(app)
