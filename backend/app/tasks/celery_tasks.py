from app.tasks.celery_app import celery_app
import asyncio


@celery_app.task(name="run_research")
def run_research_task(session_id: str, topic: str):
    asyncio.run(_async_research(session_id, topic))


async def _async_research(session_id: str, topic: str):
    from app.core.database import AsyncSessionLocal
    from app.agents.research.researcher import research_graph
    from app.models.research import ResearchSession, SessionStatus
    from app.models.agent_request import AgentStatus
    from app.models.agent import Agent
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(
                select(ResearchSession).where(ResearchSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            if not session:
                return

            session.status = SessionStatus.processing
            await db.commit()

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

            session.result = final_state["final_report"]
            session.status = SessionStatus.completed

            agents_result = await db.execute(
                select(Agent).where(Agent.session_id == session_id)
            )
            for agent in agents_result.scalars().all():
                agent.status = AgentStatus.released

            await db.commit()

        except Exception as e:
            session.status = SessionStatus.failed
            session.result = f"Research failed: {str(e)}"
            await db.commit()
            raise
