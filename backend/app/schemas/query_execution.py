from typing import Any

from pydantic import BaseModel, Field

from app.schemas.sql_validation import SqlValidationResponse


class QueryExecutionRequest(BaseModel):
    sql: str = Field(min_length=1)
    max_rows: int = Field(default=100, ge=1, le=1000)


class QueryExecutionResponse(BaseModel):
    success: bool
    validation: SqlValidationResponse
    rows: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    execution_time_ms: float | None = None
    error: str | None = None