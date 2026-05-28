"""
Celery = a task queue that runs heavy jobs in the background.

Why? Because LLM calls take 10-30 seconds.
We don't want the user's browser to hang waiting.

Instead:
1. User submits topic → API returns immediately with session_id
2. Celery runs the research in the background
3. Frontend polls for the result using session_id
"""
import asyncio
from celery import Celery
from app.core.config import settings

# Create the Celery app
celery_app = Celery(
    "cyber_hub",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC"
)


@celery_app.task(name="run_research")
def run_research_task(session_id: str, topic: str):
    """
    This runs in a background worker process.
    Calls the LangGraph research pipeline and saves results to DB.
    """
    asyncio.run(_async_research(session_id, topic))


async def _async_research(session_id: str, topic: str):
    """The actual async work — runs the LangGraph pipeline."""
    from app.core.database import AsyncSessionLocal
    from app.agents.research.research_graph import research_graph
    from app.models.models import ResearchSession, SessionStatus, Agent, AgentStatus
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        try:
            # Mark session as processing
            result = await db.execute(
                select(ResearchSession).where(ResearchSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            if not session:
                return

            session.status = SessionStatus.processing
            await db.commit()

            # Run the full research graph
            final_state = await research_graph.ainvoke({
                "topic": topic,
                "session_id": session_id,
                "plan": "",
                "agents_needed": [],
                "spawned_agents": [],
                "research_pieces": [],
                "final_report": "",
                "db": db
            })

            # Save result to DB
            session.result = final_state["final_report"]
            session.status = SessionStatus.completed

            # Release all agents that worked on this session
            agents_result = await db.execute(
                select(Agent).where(Agent.session_id == session_id)
            )
            for agent in agents_result.scalars().all():
                agent.status = AgentStatus.released

            await db.commit()

        except Exception as e:
            # If something fails, mark session as failed
            session.status = SessionStatus.failed
            session.result = f"Research failed: {str(e)}"
            await db.commit()
            raise
