from pydantic import BaseModel, Field
from typing import List, Optional


class ResearcherStructuredOutput(BaseModel):
    plan: str = Field(..., description="The research plan outlining the steps to be taken.")
    agents_needed: List[dict] = Field(..., description="A list of agents needed for the research, including their roles and skill levels.")