from fastapi import APIRouter, Depends

from app.api.auth import verify_basic_auth
from app.schemas.ask import AskRequest
from app.schemas.responses import AskResponse


router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
def ask_question(
    request: AskRequest,
    current_user: str = Depends(verify_basic_auth),
) -> AskResponse:
    return AskResponse(
        answer=f"Received your question: {request.question}",
        sql=None,
        rows=[],
        chart=None,
        assumptions=[
            "This is a Sprint 1 dummy response.",
            "No LLM or database call is happening yet.",
        ],
        followups=[
            "Next step will be connecting PostgreSQL.",
            "After that we will add SQL validation.",
        ],
    )
