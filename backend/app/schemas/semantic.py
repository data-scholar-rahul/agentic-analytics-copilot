from typing import Any
from pydantic import BaseModel, Field

class SemanticContextResponse(BaseModel):
    metrics: list[dict[str, Any]] = Field(default_factory=list)
    tables: list[dict[str, Any]] = Field(default_factory=list)
    join_rules: list[dict[str, Any]] = Field(default_factory=list)
    glossary: list[dict[str, Any]] = Field(default_factory=list)