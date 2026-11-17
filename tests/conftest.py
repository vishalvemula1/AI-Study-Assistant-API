import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Creates a FastAPI TestClient instance for running API tests.
    """
    return TestClient(app)
