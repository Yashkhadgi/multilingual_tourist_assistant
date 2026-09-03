import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.llm_wrapper import call_llm
from config.settings import RAG_MODEL

def run_rag_agent(user_message: str) -> str:
    # NOTE: this is a placeholder. Real RAG (ChromaDB retrieval) comes in Phase 4.
    system_prompt = (
        "You are the Local Info Agent of a multilingual tourist assistant. "
        "You answer questions about monuments, culture, food, and general tourist information. "
        "Respond in the same language/style the user used. "
        "Keep answers concise and factual."
    )
    return call_llm(
        model=RAG_MODEL,
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=500
    )