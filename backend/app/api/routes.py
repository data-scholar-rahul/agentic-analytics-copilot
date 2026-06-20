from fastapi import APIRouter, Depends

from app.api.auth import verify_basic_auth
from app.core.config import Settings, get_settings
from app.db.postgres_client import PostgresClient
from app.db.schema_setup import setup_database
from app.schemas.ask import AskRequest
from app.schemas.responses import AskResponse
from app.schemas.semantic import SemanticContextResponse
from app.services.semantic_service import SemanticService

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
    db = PostgresClient(database_url=settings.database_url)

    sql = """
    SELECT
        current_database() AS database_name,
        current_user AS user_name,
        version() AS postgres_version;
    """

    rows = db.execute_select(sql)

    return AskResponse(
        answer=f"Received your question: {request.question}",
        sql=sql,
        rows=rows,
        chart=None,
        assumptions=[
            "This is a Sprint 2 PostgreSQL connection test.",
            "No LLM-generated SQL is happening yet.",
            "The SQL is fixed and controlled by the backend.",
        ],
        followups=[
            "Next step will be creating application schemas.",
            "After that we will load business data.",
        ],
    )
