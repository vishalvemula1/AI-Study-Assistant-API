# AI Study Assistant API 🎓🤖

A FastAPI-powered backend for an AI Study Assistant that takes student academic questions and provides clear, structured explanations using an LLM.

---

## 📌 Features & Requirements Fulfilled

1. **FastAPI Application**:
   - `POST /ask`: Accepts student questions in JSON format and responds with structured explanations.
   - `GET /`: Health check endpoint.
   - Interactive Swagger API docs available at `/docs` and ReDoc at `/redoc`.
   - Comprehensive request validation using Pydantic.

2. **LLM Integration**:
   - Configured via environment variables loaded from `.env` using `python-dotenv`.
   - Supports OpenAI (`gpt-4o-mini`, `gpt-4o`, etc.) or any OpenAI-compatible API endpoint (Groq, vLLM, Ollama, OpenRouter).

3. **Pytest Test Suite with Mocking**:
   - Automated tests in `tests/test_main.py` verifying valid queries, invalid inputs (missing field, blank strings, wrong types), health check, and upstream LLM failure handling.
   - Mocks the LLM API calls to ensure lightning-fast, zero-cost, deterministic testing.

4. **GitHub Actions CI Pipeline**:
   - `.github/workflows/ci.yml` runs automatically on `push` and `pull_request` to `main`/`master`.
   - Installs dependencies and runs pytest with full reports.

5. **Docker Containerization**:
   - Production-ready `Dockerfile` using lightweight `python:3.12-slim`.
   - Includes container health checks and `.dockerignore` to keep image size minimal.

---

## 📂 Project Structure

```text
MLOPS EndSem Lab/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI test pipeline
├── app/
│   ├── __init__.py
│   ├── config.py                # Environment and configuration loader
│   ├── main.py                  # FastAPI application entrypoint
│   ├── schemas.py               # Pydantic models for request & response
│   └── services/
│       ├── __init__.py
│       └── llm_service.py       # LLM provider integration & prompt logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # TestClient fixtures
│   └── test_main.py             # Pytest suite with mock LLM calls
├── .dockerignore
├── .env.example                 # Example environment variables template
├── .gitignore                   # Git ignore rules for Python, venv, and secrets
├── Dockerfile                   # Docker container configuration
├── README.md                    # Documentation
└── requirements.txt             # Project dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git (optional)
- Docker (optional, for containerization)

### 2. Environment Setup (Virtual Environment)
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and set your LLM API key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
OPENAI_API_KEY=sk-...your-real-key-here...
LLM_MODEL=gpt-4o-mini
```

---

## 💻 Running the Application

Start the development server with live reload:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The API is now accessible at:
- **API URL**: http://127.0.0.1:8000
- **Interactive Swagger Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📡 API Endpoints

### 1. Ask a Study Question
- **Method**: `POST`
- **Path**: `/ask`
- **Request Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "question": "What is overfitting in machine learning and how can we prevent it?"
}
```
- **Response** (`200 OK`):
```json
{
  "question": "What is overfitting in machine learning and how can we prevent it?",
  "answer": "Overfitting happens when a model learns the training data and noise too closely, leading to poor generalization on unseen data. You can prevent it using techniques such as regularization (L1/L2), dropout, cross-validation, and gathering more training data."
}
```

- **Validation Error** (`422 Unprocessable Entity`):
If the `question` field is empty, missing, or contains only whitespace:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "question"],
      "msg": "Value error, Question cannot be empty or contain only whitespace.",
      "input": "   "
    }
  ]
}
```

### 2. Health Check
- **Method**: `GET`
- **Path**: `/`
- **Response** (`200 OK`):
```json
{
  "status": "healthy",
  "service": "AI Study Assistant API",
  "version": "1.0.0",
  "docs_url": "/docs"
}
```

---

## 🧪 Running Pytest Tests

Execute the unit tests (all LLM requests are mocked):
```bash
pytest -v
```

Output:
```text
tests/test_main.py::test_health_check PASSED                             [ 14%]
tests/test_main.py::test_ask_valid_question_success PASSED               [ 28%]
tests/test_main.py::test_ask_invalid_input_missing_field PASSED          [ 42%]
tests/test_main.py::test_ask_invalid_input_empty_string PASSED           [ 57%]
tests/test_main.py::test_ask_invalid_input_whitespace_only PASSED        [ 71%]
tests/test_main.py::test_ask_invalid_input_wrong_type PASSED             [ 85%]
tests/test_main.py::test_ask_llm_upstream_error PASSED                   [100%]
```

---

## 🐳 Docker Deployment

Build the Docker container image:
```bash
docker build -t ai-study-assistant .
```

Run the container (passing the environment variable):
```bash
docker run -d -p 8000:8000 --env-file .env --name study-assistant ai-study-assistant
```

Test the containerized endpoint:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain Big O notation."}'
```
