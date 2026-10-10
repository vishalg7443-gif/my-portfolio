import json
import os

from flask import Flask, render_template, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "entries.json")


def load_entries():
    """Load portfolio project entries from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_entry_tags(entry):
    """Return explicit tags or derive a simple category tag for a project."""
    if not isinstance(entry, dict):
        return ["Web Development"]

    tags = entry.get("tags") or entry.get("category")
    if isinstance(tags, list):
        return tags
    if tags:
        return [tags]

    title = (entry.get("title") or "").lower()
    summary = (entry.get("summary") or "").lower()
    combined = f"{title} {summary}"

    if any(keyword in combined for keyword in ["ai", "chat", "model", "agent"]):
        return ["AI"]
    if any(keyword in combined for keyword in ["data", "dashboard", "chart", "analytics"]):
        return ["Data"]
    if any(keyword in combined for keyword in ["finance", "fintech", "invest", "financial"]):
        return ["Finance"]
    if any(keyword in combined for keyword in ["flask", "web", "portfolio", "website", "app"]):
        return ["Flask"]
    if any(keyword in combined for keyword in ["game", "gaming"]):
        return ["Games"]
    if any(keyword in combined for keyword in ["design", "product", "ux", "user"]):
        return ["Product Design"]
    return ["Web Development"]


@app.route("/")
def home():
    entries = load_entries()
    added = request.args.get("added") == "1"
    return render_template(
        "index.html",
        entries=entries,
        get_entry_tags=get_entry_tags,
        added=added,
    )


@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    entries = load_entries()
    if entry_id < 0 or entry_id >= len(entries):
        return "Entry not found", 404
    return render_template(
        "entry.html",
        entry=entries[entry_id],
        entry_id=entry_id,
        get_entry_tags=get_entry_tags,
    )


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5001, debug=debug_mode)
