from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QuestionRequest, AnswerResponse
from app.services.llm_service import llm_service

app = FastAPI(
    title="AI Study Assistant API",
    description="A simple FastAPI service that answers student questions using an LLM.",
    version="1.0.0",
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Health"],
    summary="Service Health Check",
    response_description="Returns the operational status of the service",
)
def root():
    return {
        "status": "healthy",
        "service": "AI Study Assistant API",
        "version": "1.0.0",
        "docs_url": "/docs",
    }


@app.post(
    "/ask",
    response_model=AnswerResponse,
    status_code=status.HTTP_200_OK,
    tags=["AI Assistant"],
    summary="Ask a Study Question",
    response_description="Returns the original question and the LLM-generated explanation",
)
def ask_question(payload: QuestionRequest):
    """
    Accepts a question in JSON format, forwards it to the LLM service using
    the API key configured in `.env`, and returns the generated study answer.
    """
    try:
        answer = llm_service.generate_answer(payload.question)
        return AnswerResponse(question=payload.question, answer=answer)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ve),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error communicating with LLM provider: {str(exc)}",
        )
