"""
Agent Hub = the staffing agency of Cyber Hub.

Responsibilities:
1. Receive requests for agents from any department
2. Build the agent with the right role + skill level
3. Register agent in the database
4. Return the agent to the requesting department

Skill Level → determines how smart/detailed the agent's AI prompt is.
"""
import uuid
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.models import Agent, AgentRequest, SkillLevel, AgentStatus


# ── Name Generator ────────────────────────────────────────────
# Each spawned agent gets a unique name like "Nova" or "Atlas"
AGENT_NAMES = [
    "Nova", "Atlas", "Lyra", "Orion", "Sage", "Echo", "Flux",
    "Cleo", "Rex", "Zara", "Blaze", "Coda", "Dune", "Fern",
    "Gale", "Haze", "Iris", "Jade", "Kite", "Luna"
]

def generate_agent_name(role: str) -> str:
    """Give an agent a unique name based on role + random codename."""
    codename = random.choice(AGENT_NAMES)
    short_role = role.split()[0]  # "Research Analyst" → "Research"
    return f"{codename} [{short_role}]"


# ── Skill Prompt Templates ─────────────────────────────────────
# Higher skill = richer prompt = better AI output
SKILL_PROMPTS = {
    SkillLevel.junior: """
        You are a junior {role} in the {department} department at Cyber Hub.
        You handle basic tasks, follow instructions carefully, and ask questions when unsure.
        Keep responses clear and simple.
    """,
    SkillLevel.mid: """
        You are a mid-level {role} in the {department} department at Cyber Hub.
        You handle complex tasks independently, provide structured analysis,
        and consider multiple angles before concluding.
    """,
    SkillLevel.senior: """
        You are a senior {role} in the {department} department at Cyber Hub.
        You handle highly complex tasks with expertise. You provide deep analysis,
        anticipate edge cases, mentor others, and deliver comprehensive results
        with clear reasoning and actionable insights.
    """,
    SkillLevel.expert: """
        You are an expert-level {role} in the {department} department at Cyber Hub.
        You are the top authority in your field. You deliver exhaustive research,
        identify patterns others miss, synthesize across domains, and produce
        publication-quality output. Your analysis shapes strategic decisions.
    """
}


class AgentHub:
    """
    The central factory that creates agents on demand.
    Any department can call request_agent() to get a new agent.
    """

    async def request_agent(
        self,
        db: AsyncSession,
        requesting_department: str,
        role_needed: str,
        skill_level: SkillLevel,
        reason: str,
        session_id: str | None = None
    ) -> tuple[AgentRequest, Agent]:
        """
        Main method: department asks for an agent → hub builds and returns it.
        
        Returns: (request_record, new_agent)
        """

        # Step 1: Log the request in DB
        hub_request = AgentRequest(
            id=str(uuid.uuid4()),
            requesting_department=requesting_department,
            role_needed=role_needed,
            skill_level=skill_level,
            reason=reason,
            status="pending"
        )
        db.add(hub_request)
        await db.flush()  # save to DB without committing yet

        # Step 2: Build the agent
        agent = await self._spawn_agent(
            db=db,
            role=role_needed,
            department=requesting_department,
            skill_level=skill_level,
            session_id=session_id
        )

        # Step 3: Update the request as fulfilled
        hub_request.status = "fulfilled"
        hub_request.spawned_agent_id = agent.id

        await db.commit()
        await db.refresh(agent)
        await db.refresh(hub_request)

        return hub_request, agent

    async def _spawn_agent(
        self,
        db: AsyncSession,
        role: str,
        department: str,
        skill_level: SkillLevel,
        session_id: str | None
    ) -> Agent:
        """Internal: create agent record in DB."""

        agent = Agent(
            id=str(uuid.uuid4()),
            name=generate_agent_name(role),
            role=role,
            department=department,
            skill_level=skill_level,
            status=AgentStatus.idle,
            session_id=session_id
        )
        db.add(agent)
        await db.flush()
        return agent

    def get_agent_system_prompt(self, agent: Agent) -> str:
        """Build the AI system prompt based on agent's skill level."""
        template = SKILL_PROMPTS[agent.skill_level]
        return template.format(role=agent.role, department=agent.department)

    async def get_all_agents(self, db: AsyncSession) -> list[Agent]:
        """Get all agents currently in the system."""
        result = await db.execute(select(Agent).order_by(Agent.created_at.desc()))
        return list(result.scalars().all())

    async def release_agent(self, db: AsyncSession, agent_id: str):
        """Mark agent as released (work done)."""
        result = await db.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if agent:
            agent.status = AgentStatus.released
            await db.commit()


# Singleton instance — one hub for the whole app
agent_hub = AgentHub()
