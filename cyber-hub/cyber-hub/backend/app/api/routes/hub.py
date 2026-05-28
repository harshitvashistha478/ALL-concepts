"""
Agent Hub Routes:
GET  /hub/agents          → see all agents in the system
POST /hub/request-agent   → manually request a new agent (for testing)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.agents.hub.agent_hub import agent_hub
from app.schemas.schemas import AgentHubRequest, AgentHubResponse, AgentResponse

router = APIRouter(prefix="/hub", tags=["Agent Hub"])


@router.get("/agents", response_model=list[AgentResponse])
async def get_all_agents(db: AsyncSession = Depends(get_db)):
    """Returns all agents currently in the system (idle, busy, released)."""
    agents = await agent_hub.get_all_agents(db)
    return agents


@router.post("/request-agent", response_model=AgentHubResponse)
async def request_agent(
    request: AgentHubRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually request a new agent from the hub.
    Normally called internally by department Majors,
    but exposed here for testing and future department integrations.
    """
    hub_request, agent = await agent_hub.request_agent(
        db=db,
        requesting_department=request.requesting_department,
        role_needed=request.role_needed,
        skill_level=request.skill_level,
        reason=request.reason,
        session_id=request.session_id
    )

    return AgentHubResponse(
        request_id=hub_request.id,
        spawned_agent=AgentResponse.model_validate(agent),
        message=f"Agent {agent.name} ({agent.role}) spawned and sent to {request.requesting_department}"
    )
