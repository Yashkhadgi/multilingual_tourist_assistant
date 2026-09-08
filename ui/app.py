import gradio as gr
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator_graph import run_agent
from config.settings import validate_config

validate_config()

def chat_with_agent(message, history):
    session_id = "gradio-session"
    agent_name, response = run_agent(session_id, message)
    final_reply = f"**[Routed to: {agent_name}]**\n\n{response}"
    return final_reply


CUSTOM_CSS = """
:root, .dark {
    --body-background-fill: #1a1a17;
    --background-fill-primary: #1a1a17;
    --background-fill-secondary: #24241f;
    --block-background-fill: #24241f;
    --border-color-primary: #4b4b3a;
    --body-text-color: #e8e6dc;
    --block-title-text-color: #e8e6dc;
    --button-primary-background-fill: #556b2f;
    --button-primary-background-fill-hover: #6b8536;
    --button-primary-text-color: #f5f5ef;
}
body, .gradio-container {
    background-color: #1a1a17 !important;
}
.message.user {
    background-color: #556b2f !important;
    color: #f5f5ef !important;
}
.message.bot {
    background-color: #24241f !important;
    color: #e8e6dc !important;
    border: 1px solid #4b4b3a !important;
}
"""

theme = gr.themes.Base(
    primary_hue=gr.themes.colors.green,
    neutral_hue=gr.themes.colors.stone,
).set(
    body_background_fill="#1a1a17",
    block_background_fill="#24241f",
    border_color_primary="#4b4b3a",
)

demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="🧳 Multilingual Tourist Assistant",
    description="Orchestrator (LangGraph) routes between Planner Agent (maps+weather) and Info/RAG Agent (ChromaDB), with session memory.",
    theme=theme,
    css=CUSTOM_CSS,
)

if __name__ == "__main__":
    demo.launch()
