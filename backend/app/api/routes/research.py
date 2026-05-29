import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.research import ResearchSession, SessionStatus
from app.models.agent import Agent
from app.schemas.schema import ResearchRequest, ResearchResponse, ResearchResult, AgentResponse
from app.tasks.celery_tasks import run_research_task

router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/submit", response_model=ResearchResponse)
async def submit_research(
    request: ResearchRequest,
    db: AsyncSession = Depends(get_db)
):
    session = ResearchSession(
        id=str(uuid.uuid4()),
        user_id=request.user_id,
        topic=request.topic,
        status=SessionStatus.pending
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    run_research_task.delay(session.id, request.topic)

    return ResearchResponse(
        session_id=session.id,
        status=session.status,
        topic=session.topic,
        message="Research started! Agents are being assembled..."
    )


@router.get("/{session_id}", response_model=ResearchResult)
async def get_research_result(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ResearchSession).where(ResearchSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    agents_result = await db.execute(
        select(Agent).where(Agent.session_id == session_id)
    )
    agents = list(agents_result.scalars().all())

    return ResearchResult(
        session_id=session.id,
        status=session.status,
        topic=session.topic,
        result=session.result,
        agents_used=[AgentResponse.model_validate(a) for a in agents]
    )


@router.get("/history/{user_id}")
async def get_user_history(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ResearchSession)
        .where(ResearchSession.user_id == user_id)
        .order_by(ResearchSession.created_at.desc())
    )
    sessions = list(result.scalars().all())
    return sessions

