from unittest.mock import MagicMock
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """
    Verify the root health check endpoint returns 200 and healthy status.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI Study Assistant API"


def test_ask_valid_question_success(client: TestClient, mocker):
    """
    Test Case 1: Valid input with mocked LLM response.
    Verifies that the /ask endpoint accepts a question, delegates to the
    LLM service, and returns 200 OK with the generated answer.
    """
    mock_answer = (
        "Gradient descent is an optimization algorithm used to minimize a loss function "
        "by iteratively moving in the direction of steepest descent."
    )
    # Mock the LLM service generate_answer method
    mock_generate = mocker.patch(
        "app.main.llm_service.generate_answer",
        return_value=mock_answer,
    )

    payload = {"question": "What is gradient descent?"}
    response = client.post("/ask", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is gradient descent?"
    assert data["answer"] == mock_answer

    # Verify that mock was called once with the exact question
    mock_generate.assert_called_once_with("What is gradient descent?")


def test_ask_invalid_input_missing_field(client: TestClient):
    """
    Test Case 2: Invalid input (empty JSON object / missing question field).
    Verifies that the /ask endpoint returns 422 Unprocessable Entity.
    """
    response = client.post("/ask", json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_ask_invalid_input_empty_string(client: TestClient):
    """
    Test Case 3: Invalid input (empty string question).
    Verifies that blank questions are rejected with 422 Unprocessable Entity.
    """
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_ask_invalid_input_whitespace_only(client: TestClient):
    """
    Test Case 4: Invalid input (whitespace-only question).
    Verifies that questions with only spaces are rejected with 422 Unprocessable Entity.
    """
    response = client.post("/ask", json={"question": "     "})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_ask_invalid_input_wrong_type(client: TestClient):
    """
    Test Case 5: Invalid input (non-string question).
    Verifies that numeric/array values are rejected with 422 Unprocessable Entity.
    """
    response = client.post("/ask", json={"question": 12345})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_ask_llm_upstream_error(client: TestClient, mocker):
    """
    Test Case 6: Upstream LLM failure handling.
    Verifies that external LLM communication exceptions return 502 Bad Gateway.
    """
    mocker.patch(
        "app.main.llm_service.generate_answer",
        side_effect=RuntimeError("Connection refused by OpenAI API"),
    )

    payload = {"question": "Explain Docker containerization."}
    response = client.post("/ask", json=payload)

    assert response.status_code == 502
    data = response.json()
    assert "Error communicating with LLM provider" in data["detail"]
