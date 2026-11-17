from pydantic import BaseModel, Field, field_validator


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="The student's study or academic question to be answered by the assistant",
        examples=["What is the difference between supervised and unsupervised learning?"]
    )

    @field_validator("question")
    @classmethod
    def validate_question_not_blank(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Question cannot be empty or contain only whitespace.")
        return trimmed


class AnswerResponse(BaseModel):
    question: str = Field(
        ...,
        description="The original student question"
    )
    answer: str = Field(
        ...,
        description="The generated explanation or answer from the LLM"
    )
