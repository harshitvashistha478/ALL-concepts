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



class AgentRequest(Base):
    __tablename__ = "agent_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    requesting_department: Mapped[str] = mapped_column(String(100))
    role_needed: Mapped[str] = mapped_column(String(100))
    skill_level: Mapped[SkillLevel] = mapped_column(Enum(SkillLevel))
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")  
    spawned_agent_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)