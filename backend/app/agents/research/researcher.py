import json
from typing import TypedDict, Annotated
import operator

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END, START

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.agents_hub.hub import agent_hub
from app.models.agent import Agent, SkillLevel, AgentStatus
from app.core.config import settings
from app.utils.agents_extras import get_llm
from app.utils.agents_prompt import major_researcher_system_prompt
from app.utils.structured_output_file import ResearcherStructuredOutput


class ResearchState(TypedDict):
    topic: str                          
    session_id: str
    plan: str                         
    agents_needed: list[dict]           
    spawned_agents: list[Agent]        
    research_pieces: Annotated[list[str], operator.add]
    final_report: str                  
    db: object 


async def major_planning_node(state: ResearchState) -> dict:
    llm = get_llm(department_model="researcher")
    researcher_llm = llm.with_structured_output(ResearcherStructuredOutput)
    
    try:
        response = await researcher_llm.ainvoke([
            SystemMessage(content=major_researcher_system_prompt),
            HumanMessage(content=f"Topic to research: {state['topic']}")
        ])

        return {
            "plan": response.plan,
            "agents_needed": response.agents_needed
        }

    except Exception as e:
        print(f"Error in major_planning_node: {e}")
        return {
            "plan": f"Research the topic: {state['topic']}",
            "agents_needed": [
                {"role": "Research Analyst", "skill_level": "mid", "focus": state["topic"]}
            ]
        }
    

async def spawn_agents_node(state: ResearchState) -> dict:
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


async def research_node(state: ResearchState) -> dict:
    llm = get_llm()
    pieces = []

    for i, agent in enumerate(state["spawned_agents"]):
        focus = state["agents_needed"][i].get("focus", state["topic"]) if i < len(state["agents_needed"]) else state["topic"]

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

        agent.status = AgentStatus.busy

    return {"research_pieces": pieces}


async def synthesize_node(state: ResearchState) -> dict:
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


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("major_planning", major_planning_node)
    graph.add_node("spawn_agents", spawn_agents_node)
    graph.add_node("research", research_node)
    graph.add_node("synthesize", synthesize_node)

    graph.add_edge(START, "major_planning")
    graph.add_edge("major_planning", "spawn_agents")
    graph.add_edge("spawn_agents", "research")
    graph.add_edge("research", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


research_graph = build_research_graph()