from fastapi import APIRouter, Depends

from app.api.auth import verify_basic_auth
from app.core.config import Settings, get_settings
from app.db.postgres_client import PostgresClient
from app.db.schema_setup import setup_database
from app.schemas.ask import AskRequest
from app.schemas.responses import AskResponse
from app.schemas.semantic import SemanticContextResponse
from app.services.semantic_service import SemanticService
from app.schemas.sql_validation import SqlValidationRequest, SqlValidationResponse
from app.services.sql_validator import SqlValidator
from app.schemas.query_execution import QueryExecutionRequest, QueryExecutionResponse
from app.services.query_execution_service import QueryExecutionService
from app.services.intent_router import IntentRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/admin/setup-database")
def setup_database_endpoint(
    current_user: str = Depends(verify_basic_auth),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    db = PostgresClient(database_url=settings.database_url)
    setup_database(db)

    return {
        "status": "ok",
        "message": "Database schemas and foundational tables created.",
    }

@router.get("/admin/semantic-context", response_model= SemanticContextResponse)
def get_semantic_context_endpoint(current_user: str = Depends(verify_basic_auth), settings: Settings = Depends(get_settings)) -> SemanticContextResponse:
    db = PostgresClient(database_url=settings.database_url)
    semantic_service = SemanticService(db=db)
    return semantic_service.get_semantic_context()

@router.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    current_user: str = Depends(verify_basic_auth),
    settings: Settings = Depends(get_settings),
) -> AskResponse:
    intent_router = IntentRouter()
    matched_intent = intent_router.match(request.question)

    if matched_intent is None:
        return AskResponse(
            answer=(
                "I can answer only a few supported analytics questions right now. "
                "Try: 'Show order count by status', 'Show revenue by month', "
                "or 'Show top product categories by revenue'."
            ),
            assumptions=[
                "Sprint 10 uses deterministic keyword matching.",
                "No LLM-generated SQL is being used yet.",
            ],
            followups=[
                "Show order count by status",
                "Show revenue by month",
                "Show top product categories by revenue",
            ],
        )

    db = PostgresClient(database_url=settings.database_url)
    validator = SqlValidator()
    query_execution_service = QueryExecutionService(
        db=db,
        validator=validator,
    )

    execution_result = query_execution_service.execute(
        sql=matched_intent.sql,
        max_rows=100,
    )

    if not execution_result.success:
        return AskResponse(
            answer="I matched your question, but the query could not be executed.",
            sql=execution_result.validation.normalized_sql,
            rows=[],
            assumptions=[
                f"Matched intent: {matched_intent.intent_name}",
                f"Validation status: {execution_result.validation.is_valid}",
            ],
            followups=[
                "Check the backend logs.",
                "Test the SQL through /admin/execute-sql.",
            ],
        )

    return AskResponse(
        answer=matched_intent.answer_template,
        sql=execution_result.validation.normalized_sql,
        rows=execution_result.rows,
        assumptions=[
            f"Matched intent: {matched_intent.intent_name}",
            "SQL is fixed by backend intent routing.",
            "SQL was validated before execution.",
        ],
        followups=[
            "Try asking another supported analytics question.",
        ],
    )

@router.post("/admin/validate-sql", response_model=SqlValidationResponse)
def validate_sql_endpoint(
    request: SqlValidationRequest,
    current_user: str = Depends(verify_basic_auth),
) -> SqlValidationResponse:
    validator = SqlValidator()
    return validator.validate(request.sql)

@router.post("/admin/execute-sql", response_model=QueryExecutionResponse)
def execute_sql_endpoint(
    request: QueryExecutionRequest,
    current_user: str = Depends(verify_basic_auth),
    settings: Settings = Depends(get_settings),
) -> QueryExecutionResponse:
    db = PostgresClient(database_url=settings.database_url)
    validator = SqlValidator()
    query_execution_service = QueryExecutionService(
        db=db,
        validator=validator,
    )

    return query_execution_service.execute(
        sql=request.sql,
        max_rows=request.max_rows,
    )