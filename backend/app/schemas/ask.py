from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=3,
        description="Natural language analytics question from the user",
    )

    conversation_id: str | None = Field(
        default=None,
        description="Optional conversation id for continuing a chat",
    )
