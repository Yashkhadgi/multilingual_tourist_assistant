import gradio as gr
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import route_query
from config.settings import validate_config

validate_config()

def chat_with_agent(message, history):
    agent_name, response = route_query(message)
    # Shows which agent handled it — early version of the reasoning trace feature
    final_reply = f"**[Routed to: {agent_name}]**\n\n{response}"
    return final_reply

demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="🧳 Multilingual Tourist Assistant (Phase 2)",
    description="Orchestrator now routes between Planner Agent and Info/RAG Agent."
)

if __name__ == "__main__":
    demo.launch()