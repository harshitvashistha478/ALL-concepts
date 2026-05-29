from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.agents.agents_hub.hub import agent_hub
from app.schemas.schema import AgentHubRequest, AgentHubResponse, AgentResponse


router = APIRouter(prefix="/hub", tags=["Agent Hub"])


@router.get("/agents", response_model=list[AgentResponse])
async def get_all_agents(db: AsyncSession = Depends(get_db)):
    agents = await agent_hub.get_all_agents(db)
    return agents


@router.post("/request-agent", response_model=AgentHubResponse)
async def request_agent(
    request: AgentHubRequest,
    db: AsyncSession = Depends(get_db)
):
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


