from pydantic import BaseModel, Field


class SqlValidationRequest(BaseModel):
    sql: str = Field(min_length=1)


class SqlValidationResponse(BaseModel):
    is_valid: bool
    reason: str
    normalized_sql: str | None = None