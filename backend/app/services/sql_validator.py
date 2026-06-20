import re

from app.schemas.sql_validation import SqlValidationResponse


class SqlValidator:
    blocked_keywords = {
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
        "grant",
        "revoke",
        "copy",
        "execute",
        "call",
    }

    allowed_schemas = {
        "mart",
        "semantic",
    }

    blocked_schemas = {
        "raw",
        "agent_ops",
        "public",
        "pg_catalog",
        "information_schema",
    }

    def validate(self, sql: str) -> SqlValidationResponse:
        normalized_sql = self._normalize_sql(sql)
        lowercase_sql = normalized_sql.lower()

        if not normalized_sql:
            return SqlValidationResponse(
                is_valid=False,
                reason="SQL is empty.",
            )

        if ";" in normalized_sql.rstrip(";"):
            return SqlValidationResponse(
                is_valid=False,
                reason="Multiple SQL statements are not allowed.",
            )

        normalized_sql = normalized_sql.rstrip(";").strip()
        lowercase_sql = normalized_sql.lower()

        if not lowercase_sql.startswith("select "):
            return SqlValidationResponse(
                is_valid=False,
                reason="Only SELECT queries are allowed.",
            )

        blocked_keyword = self._find_blocked_keyword(lowercase_sql)
        if blocked_keyword:
            return SqlValidationResponse(
                is_valid=False,
                reason=f"Blocked SQL keyword found: {blocked_keyword}.",
            )

        blocked_schema = self._find_blocked_schema(lowercase_sql)
        if blocked_schema:
            return SqlValidationResponse(
                is_valid=False,
                reason=f"Blocked schema referenced: {blocked_schema}.",
            )

        has_allowed_schema = self._has_allowed_schema_reference(lowercase_sql)
        if not has_allowed_schema:
            return SqlValidationResponse(
                is_valid=False,
                reason="Query must reference at least one allowed schema: mart or semantic.",
            )

        return SqlValidationResponse(
            is_valid=True,
            reason="SQL passed basic validation.",
            normalized_sql=normalized_sql,
        )

    def _normalize_sql(self, sql: str) -> str:
        return " ".join(sql.strip().split())

    def _find_blocked_keyword(self, lowercase_sql: str) -> str | None:
        for keyword in self.blocked_keywords:
            pattern = rf"\b{keyword}\b"
            if re.search(pattern, lowercase_sql):
                return keyword
        return None

    def _find_blocked_schema(self, lowercase_sql: str) -> str | None:
        for schema in self.blocked_schemas:
            pattern = rf"\b{schema}\."
            if re.search(pattern, lowercase_sql):
                return schema
        return None

    def _has_allowed_schema_reference(self, lowercase_sql: str) -> bool:
        for schema in self.allowed_schemas:
            pattern = rf"\b{schema}\."
            if re.search(pattern, lowercase_sql):
                return True
        return False