from openai import OpenAI
from app.config import OPENAI_API_KEY, LLM_MODEL, LLM_BASE_URL


class LLMService:
    """
    Service responsible for interacting with the LLM API to generate answers
    to students' academic questions.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or LLM_MODEL
        self.base_url = base_url or LLM_BASE_URL
        self._client: OpenAI | None = None

    def get_client(self) -> OpenAI:
        """
        Instantiates or returns the OpenAI client instance using the configured API key.
        """
        if not self.api_key or self.api_key.strip() == "" or self.api_key == "your_openai_api_key_here":
            raise ValueError(
                "OPENAI_API_KEY is not configured. Please set a valid OPENAI_API_KEY in your .env file."
            )

        if self._client is None:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        return self._client

    def generate_answer(self, question: str) -> str:
        """
        Sends the question to the LLM and returns the generated study explanation.
        """
        client = self.get_client()

        system_prompt = (
            "You are a friendly, highly knowledgeable AI Study Assistant. "
            "Help students understand concepts clearly by providing structured, "
            "accurate, and easy-to-digest explanations with examples where helpful."
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content
        if not content:
            return "No response could be generated for this question."

        return content.strip()


# Singleton instance for application use
llm_service = LLMService()
