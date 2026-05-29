import uuid
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.agent import Agent, SkillLevel, AgentStatus
from app.models.agent_request import AgentRequest
from app.utils.agents_extras import AGENT_NAMES
from app.utils.agents_prompt import SKILL_PROMPTS


def generate_agent_name(role: str) -> str:
    """Give an agent a unique name based on role + random codename."""
    codename = random.choice(AGENT_NAMES)
    short_role = role.split()[0]  
    return f"{codename} [{short_role}]"


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

        hub_request = AgentRequest(
            id=str(uuid.uuid4()),
            requesting_department=requesting_department,
            role_needed=role_needed,
            skill_level=skill_level,
            reason=reason,
            status="pending"
        )

        db.add(hub_request)
        await db.flush()  

        created_agent = await self._spawn_agent(
            db=db,
            role=role_needed,
            department=requesting_department,
            skill_level=skill_level,
            session_id=session_id
        )

        hub_request.status = "fulfilled"
        hub_request.spawned_agent_id = created_agent.id
        await db.commit()
        await db.refresh(created_agent)

        return hub_request, created_agent
    

    async def _spawn_agent(
        self,
        db: AsyncSession,
        role: str,
        department: str,
        skill_level: SkillLevel,
        session_id: str | None
    ) -> Agent:
        """Internal method to create and save a new agent based on specs."""
        
        name = generate_agent_name(role)

        new_agent = Agent(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
            department=department,
            skill_level=skill_level,
            status=AgentStatus.idle,
            session_id=session_id
        )

        db.add(new_agent)
        await db.flush()  
        return new_agent
    

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


agent_hub = AgentHub()