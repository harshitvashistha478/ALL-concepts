from pydantic import BaseModel
from datetime import datetime
from app.models.research import SessionStatus
from app.models.agent import SkillLevel, AgentStatus


class UserCreate(BaseModel):
    pass  

class UserResponse(BaseModel):
    id: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    department: str
    skill_level: SkillLevel
    status: AgentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class AgentHubRequest(BaseModel):
    requesting_department: str
    role_needed: str
    skill_level: SkillLevel
    reason: str
    session_id: str | None = None

class AgentHubResponse(BaseModel):
    request_id: str
    spawned_agent: AgentResponse
    message: str


class ResearchRequest(BaseModel):
    user_id: str
    topic: str

class ResearchResponse(BaseModel):
    session_id: str
    status: SessionStatus
    topic: str
    message: str

class ResearchResult(BaseModel):
    session_id: str
    status: SessionStatus
    topic: str
    result: str | None
    agents_used: list[AgentResponse]
