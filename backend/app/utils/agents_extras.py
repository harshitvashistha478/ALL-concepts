from langchain_groq import ChatGroq
from app.core.config import settings


from app.models.agent import SkillLevel


AGENT_NAMES = [
    "Nova", "Atlas", "Lyra", "Orion", "Sage", "Echo", "Flux",
    "Cleo", "Rex", "Zara", "Blaze", "Coda", "Dune", "Fern",
    "Gale", "Haze", "Iris", "Jade", "Kite", "Luna"
]


def get_llm(department_model: str = "researcher") -> ChatGroq:
    return ChatGroq(
        model=getattr(settings, f"{department_model.upper()}_MODEL", settings.GROQ_MODEL),
        api_key=settings.GROQ_API_KEY
    )