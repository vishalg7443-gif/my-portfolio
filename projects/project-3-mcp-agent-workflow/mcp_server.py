from fastmcp import FastMCP

mcp = FastMCP("Vishal Tool Server")


@mcp.tool()
def greet(name: str = "friend") -> str:
    """Greet a person by name."""
    return f"Hey {name}! Great to see you."


@mcp.tool()
def get_schedule(day: str = "today") -> dict:
    """Return a lightweight schedule for a requested day."""
    return {
        "day": day,
        "events": [
            "9:00 — Deep work",
            "12:30 — Lunch",
            "3:00 — Project build session",
        ],
    }


@mcp.tool()
def get_hype(topic: str = "your project") -> str:
    """Generate a short motivational message about a topic."""
    return f"{topic.title()} is moving in the right direction — keep shipping."


if __name__ == "__main__":
    mcp.run()
