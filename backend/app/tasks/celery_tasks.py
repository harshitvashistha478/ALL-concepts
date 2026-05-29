from app.tasks.celery_app import celery_app
import asyncio
import traceback


@celery_app.task(name="run_research")
def run_research_task(session_id: str, topic: str):
    asyncio.run(_async_research(session_id, topic))


async def _async_research(session_id: str, topic: str):
    from app.core.database import AsyncSessionLocal
    from app.agents.research.researcher import research_graph
    import app.models as models
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        session = None
        try:
            result = await db.execute(
                select(models.ResearchSession).where(models.ResearchSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            if not session:
                return

            session.status = models.SessionStatus.processing
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
            session.status = models.SessionStatus.completed

            agents_result = await db.execute(
                select(models.Agent).where(models.Agent.session_id == session_id)
            )
            for agent in agents_result.scalars().all():
                agent.status = models.AgentStatus.released

            await db.commit()

        except Exception as e:
            traceback.print_exc()

            if session:
                session.status = models.SessionStatus.failed
                session.result = f"Research failed: {str(e)}"
                await db.commit()

            raise
