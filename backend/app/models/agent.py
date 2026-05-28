import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum as py_enum
from app.core.database import Base


class SkillLevel(str, py_enum.Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"
    expert = "expert"


class AgentStatus(str, py_enum.Enum):
    idle = "idle"      
    busy = "busy"      
    released = "released" 


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)       # e.g. "Research Analyst"
    department: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "research"
    skill_level: Mapped[SkillLevel] = mapped_column(Enum(SkillLevel), default=SkillLevel.mid)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus), default=AgentStatus.idle)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session_id: Mapped[str | None] = mapped_column(String, ForeignKey("research_sessions.id"), nullable=True)