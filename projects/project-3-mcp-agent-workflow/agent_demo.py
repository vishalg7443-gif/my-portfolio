from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[..., Any]


def greet(name: str = "friend") -> dict:
    return {"message": f"Hey {name}! Great to see you."}


def get_schedule(day: str = "today") -> dict:
    return {
        "day": day,
        "events": [
            "9:00 — Deep work",
            "12:30 — Lunch",
            "3:00 — Project build session",
        ],
    }


def get_hype(topic: str = "your project") -> dict:
    return {"message": f"{topic.title()} is moving in the right direction — keep shipping."}


TOOLS = {
    "greet": Tool("greet", "Greet a person", greet),
    "get_schedule": Tool("get_schedule", "Return a simple schedule", get_schedule),
    "get_hype": Tool("get_hype", "Generate short motivational feedback", get_hype),
}


def choose_tool(user_request: str) -> tuple[str, dict]:
    text = user_request.lower()
    if any(word in text for word in ["schedule", "calendar", "today", "tomorrow"]):
        return "get_schedule", {"day": "today"}
    if any(word in text for word in ["hype", "motivate", "encourage", "energy"]):
        return "get_hype", {"topic": user_request}
    return "greet", {"name": "builder"}


def run_agent(user_request: str) -> dict:
    tool_name, args = choose_tool(user_request)
    tool = TOOLS[tool_name]
    result = tool.fn(**args)
    return {
        "request": user_request,
        "selected_tool": tool_name,
        "arguments": args,
        "tool_result": result,
        "final_response": f"I used {tool_name} to help with your request: {result}",
    }


if __name__ == "__main__":
    prompt = input("Ask the agent something: ")
    print(run_agent(prompt))
