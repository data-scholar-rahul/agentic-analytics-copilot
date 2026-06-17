from typing import Any

from pydantic import BaseModel, Field


class AskResponse(BaseModel):
    answer: str
    sql: str | None = None
    rows: list[dict[str, Any]] = Field(default_factory=list)
    chart: dict[str, Any] | None = None
    assumptions: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)
