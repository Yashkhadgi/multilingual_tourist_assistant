import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.llm_wrapper import call_llm
from config.settings import PLANNER_MODEL

def run_planner_agent(user_message: str) -> str:
    system_prompt = (
        "You are the Planner Agent of a multilingual tourist assistant. "
        "You specialize in creating day-wise travel itineraries. "
        "Respond in the same language/style the user used. "
        "Keep it structured and practical."
    )
    return call_llm(
        model=PLANNER_MODEL,
        system_prompt=system_prompt,
        user_message=user_message,
        max_tokens=800
    )