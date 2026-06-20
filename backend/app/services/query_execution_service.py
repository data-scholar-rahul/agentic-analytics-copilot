import time

from app.db.postgres_client import PostgresClient
from app.schemas.query_execution import QueryExecutionResponse
from app.schemas.sql_validation import SqlValidationResponse
from app.services.sql_validator import SqlValidator


class QueryExecutionService:
    def __init__(self, db: PostgresClient, validator: SqlValidator):
        self.db = db
        self.validator = validator

    def execute(self, sql: str, max_rows: int = 100) -> QueryExecutionResponse:
        validation = self.validator.validate(sql)

        if not validation.is_valid:
            return QueryExecutionResponse(
                success=False,
                validation=validation,
                error=validation.reason,
            )

        executable_sql = self._apply_limit(
            sql=validation.normalized_sql or sql,
            max_rows=max_rows,
        )

        start_time = time.perf_counter()

        try:
            rows = self.db.execute_select(executable_sql)
        except Exception as exc:
            execution_time_ms = self._elapsed_ms(start_time)

            return QueryExecutionResponse(
                success=False,
                validation=validation,
                rows=[],
                row_count=0,
                execution_time_ms=execution_time_ms,
                error=str(exc),
            )

        execution_time_ms = self._elapsed_ms(start_time)

        return QueryExecutionResponse(
            success=True,
            validation=validation,
            rows=rows,
            row_count=len(rows),
            execution_time_ms=execution_time_ms,
            error=None,
        )

    def _apply_limit(self, sql: str, max_rows: int) -> str:
        lowercase_sql = sql.lower()

        if " limit " in lowercase_sql:
            return sql

        return f"{sql} LIMIT {max_rows}"

    def _elapsed_ms(self, start_time: float) -> float:
        return round((time.perf_counter() - start_time) * 1000, 2)