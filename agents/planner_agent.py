import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.llm_wrapper import call_llm
from tools.maps_tool import nearby_attractions
from tools.weather_tool import get_forecast
from config.settings import PLANNER_MODEL


def _extract_destination(user_message: str) -> str:
    result = call_llm(
        model=PLANNER_MODEL,
        system_prompt="Extract ONLY the destination city/place name mentioned in this travel request. Respond with just the place name, nothing else.",
        user_message=user_message,
        max_tokens=20,
    )
    return result.strip()


def run_planner_agent(user_message: str, history: str = "") -> str:
    destination = _extract_destination(user_message)

    attractions = nearby_attractions(destination) if destination else []
    forecast = get_forecast(destination) if destination else []

    tool_context = ""
    if attractions:
        tool_context += "Nearby attractions (from Google Maps):\n"
        tool_context += "\n".join(f"- {a['name']} ({a.get('rating', 'N/A')}★) - {a['address']}" for a in attractions)
        tool_context += "\n\n"
    if forecast:
        tool_context += "Weather forecast:\n"
        tool_context += "\n".join(f"- {f['date']}: {f['temp_min']}-{f['temp_max']}°C, {f['condition']}" for f in forecast)
        tool_context += "\n\n"

    system_prompt = (
        "You are the Planner Agent of a multilingual tourist assistant. "
        "You create day-wise travel itineraries. "
        "If tool data (attractions, weather) is provided below, weave it into a practical plan — "
        "e.g. suggest indoor activities on rainy-forecast days, prioritize highly-rated nearby attractions. "
        "If no tool data is available, plan from general knowledge and mention that live data wasn't available. "
        "Respond in the same language/style the user used. Keep it structured (Day 1, Day 2, ...) and practical.\n\n"
        f"{tool_context}"
        + (f"Recent conversation:\n{history}\n\n" if history else "")
    )

    return call_llm(model=PLANNER_MODEL, system_prompt=system_prompt, user_message=user_message, max_tokens=1500)


if __name__ == "__main__":
    print(run_planner_agent("Plan a 3 day trip to Udaipur"))
