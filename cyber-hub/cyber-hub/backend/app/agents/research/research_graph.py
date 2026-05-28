"""
Research Area — How it works:

1. User sends a topic
2. Research Major (AI) reads the topic and decides what agents are needed
3. Major sends requests to Agent Hub for those agents
4. Each spawned agent does its part of the research using LangGraph
5. Results are combined and returned to user

LangGraph = a way to build AI workflows as a graph (nodes + edges).
Each node = one step in the process.
"""
import json
from typing import TypedDict, Annotated
import operator

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.hub.agent_hub import agent_hub
from app.models.models import Agent, SkillLevel, AgentStatus
from app.core.config import settings


# ── LangGraph State ───────────────────────────────────────────
# This is the "memory" that flows through all nodes in the graph.
# Each node can read and update this state.
class ResearchState(TypedDict):
    topic: str                          # what to research
    session_id: str
    plan: str                           # Major's research plan
    agents_needed: list[dict]           # roles Major decided to spawn
    spawned_agents: list[Agent]         # actual agents from hub
    research_pieces: Annotated[list[str], operator.add]  # each agent's output
    final_report: str                   # synthesized final result
    db: object                          # DB session passed through


# ── LLM Setup ─────────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama3-8b-8192",   # Free, fast Llama3 model on Groq
        temperature=0.7
    )


# ── Node 1: Research Major ────────────────────────────────────
async def major_planning_node(state: ResearchState) -> dict:
    """
    The Major reads the topic and creates a research plan.
    Decides how many agents are needed and what their roles are.
    Returns structured JSON so we can parse it programmatically.
    """
    llm = get_llm()

    system_prompt = """
    You are the Research Major at Cyber Hub — the team lead of the Research Area.
    When given a research topic, you must:
    1. Break it into 2-3 focused sub-topics
    2. Decide what researcher roles are needed (e.g. "Data Analyst", "Domain Expert", "Fact Checker")
    3. Assign a skill level to each: junior, mid, senior, or expert

    Respond ONLY with valid JSON in this exact format:
    {
        "plan": "One sentence describing your research strategy",
        "agents_needed": [
            {"role": "Role Name", "skill_level": "mid", "focus": "What this agent will research"}
        ]
    }
    """

    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Topic to research: {state['topic']}")
    ])

    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback if LLM doesn't return perfect JSON
        parsed = {
            "plan": f"Research the topic: {state['topic']}",
            "agents_needed": [
                {"role": "Research Analyst", "skill_level": "mid", "focus": state["topic"]}
            ]
        }

    return {
        "plan": parsed["plan"],
        "agents_needed": parsed["agents_needed"]
    }


# ── Node 2: Request Agents from Hub ──────────────────────────
async def spawn_agents_node(state: ResearchState) -> dict:
    """
    For each agent the Major decided is needed,
    send a request to Agent Hub and get a real agent back.
    """
    db: AsyncSession = state["db"]
    spawned = []

    for agent_spec in state["agents_needed"]:
        skill = SkillLevel(agent_spec.get("skill_level", "mid"))

        _, agent = await agent_hub.request_agent(
            db=db,
            requesting_department="research",
            role_needed=agent_spec["role"],
            skill_level=skill,
            reason=agent_spec.get("focus", "General research"),
            session_id=state["session_id"]
        )
        spawned.append(agent)

    return {"spawned_agents": spawned}


# ── Node 3: Each Agent Does Research ─────────────────────────
async def research_node(state: ResearchState) -> dict:
    """
    Each spawned agent gets its own AI call to research its focus area.
    The skill level determines the quality of its system prompt.
    All results are collected as research_pieces.
    """
    llm = get_llm()
    pieces = []

    for i, agent in enumerate(state["spawned_agents"]):
        focus = state["agents_needed"][i].get("focus", state["topic"]) if i < len(state["agents_needed"]) else state["topic"]

        # Get the prompt matching this agent's skill level
        system_prompt = agent_hub.get_agent_system_prompt(agent)

        response = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
                Research Plan: {state['plan']}
                Your specific focus: {focus}
                Overall topic: {state['topic']}
                
                Provide a detailed, well-structured research piece on your focus area.
                Be thorough. Use sections. Include key facts, insights, and conclusions.
            """)
        ])

        pieces.append(f"## {agent.name} ({agent.role})\n{response.content}")

        # Mark agent as busy in DB
        agent.status = AgentStatus.busy

    return {"research_pieces": pieces}


# ── Node 4: Synthesize Final Report ──────────────────────────
async def synthesize_node(state: ResearchState) -> dict:
    """
    Takes all individual research pieces and combines them
    into one coherent final report for the user.
    """
    llm = get_llm()

    combined = "\n\n".join(state["research_pieces"])

    response = await llm.ainvoke([
        SystemMessage(content="""
            You are a senior research synthesizer at Cyber Hub.
            You receive research pieces from multiple agents and combine them
            into one cohesive, well-structured final report.
            Format it clearly with:
            - Executive Summary
            - Key Findings (from each agent's work)
            - Overall Conclusion
            Make it readable and insightful.
        """),
        HumanMessage(content=f"""
            Topic: {state['topic']}
            Research Plan: {state['plan']}
            
            Individual Research Pieces:
            {combined}
            
            Synthesize these into one final comprehensive report.
        """)
    ])

    return {"final_report": response.content}


# ── Build the LangGraph ───────────────────────────────────────
def build_research_graph():
    """
    Assembles the nodes into a graph (a flow chart of steps).
    
    Flow:
    Major Plans → Spawn Agents → Do Research → Synthesize → END
    """
    graph = StateGraph(ResearchState)

    graph.add_node("major_planning", major_planning_node)
    graph.add_node("spawn_agents", spawn_agents_node)
    graph.add_node("research", research_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("major_planning")
    graph.add_edge("major_planning", "spawn_agents")
    graph.add_edge("spawn_agents", "research")
    graph.add_edge("research", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


# Compile once, reuse everywhere
research_graph = build_research_graph()
