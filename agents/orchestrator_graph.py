import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

from tools.llm_wrapper import call_llm
from config.settings import ORCHESTRATOR_MODEL
from agents.planner_agent import run_planner_agent
from agents.rag_agent import run_rag_agent
from memory.session_memory import save_turn, format_history


# Define the shared state that flows through the graph
class AgentState(TypedDict):
    session_id: str
    user_message: str
    intent: str
    agent_used: str
    response: str


# Node 1: Classify intent
def classify_node(state: AgentState) -> AgentState:
    system_prompt = (
        "You are an intent classifier for a tourist assistant. "
        "Classify the user's message into exactly ONE of these categories:\n"
        "- 'planner' : if the user wants an itinerary, trip plan, schedule, or travel route\n"
        "- 'info' : if the user is asking about a place, monument, culture, food, or general tourist information\n\n"
        "Respond with ONLY the single word: planner OR info. No explanation, no punctuation."
    )
    result = call_llm(
        model=ORCHESTRATOR_MODEL,
        system_prompt=system_prompt,
        user_message=state["user_message"],
        max_tokens=10
    )
    intent = result.strip().lower()
    if intent not in ["planner", "info"]:
        intent = "info"

    state["intent"] = intent
    return state


# Node 2: Planner agent
def planner_node(state: AgentState) -> AgentState:
    history = format_history(state["session_id"])
    state["response"] = run_planner_agent(state["user_message"], history=history)
    state["agent_used"] = "Planner Agent"
    return state


# Node 3: RAG/Info agent
def rag_node(state: AgentState) -> AgentState:
    history = format_history(state["session_id"])
    state["response"] = run_rag_agent(state["user_message"], history=history)
    state["agent_used"] = "Info/RAG Agent"
    return state


# Conditional routing function — decides which node runs next
def route_decision(state: AgentState) -> Literal["planner", "info"]:
    return state["intent"]


# Build the graph
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("planner", planner_node)
    graph.add_node("info", rag_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_decision,
        {
            "planner": "planner",
            "info": "info"
        }
    )

    graph.add_edge("planner", END)
    graph.add_edge("info", END)

    return graph.compile()


# Compiled app — import this in ui/app.py
tourist_agent_graph = build_graph()


def run_agent(session_id: str, user_message: str):
    save_turn(session_id, "user", user_message)

    initial_state = {
        "session_id": session_id,
        "user_message": user_message,
        "intent": "",
        "agent_used": "",
        "response": ""
    }
    final_state = tourist_agent_graph.invoke(initial_state)

    save_turn(session_id, "assistant", final_state["response"])
    return final_state["agent_used"], final_state["response"]


if __name__ == "__main__":
    agent, reply = run_agent("test-session", "Plan a 3 day trip to Udaipur")
    print(f"Agent used: {agent}")
    print(f"Reply: {reply}")
