import json
import os
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "entries.json")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "images", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_entries():
    """Load all journal entries from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entries(entries):
    """Save entries to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def get_entry_tags(entry):
    """Derive a simple category tag for each project entry."""
    if not isinstance(entry, dict):
        return ["Web Development"]

    tags = entry.get("tags") or entry.get("category")
    if isinstance(tags, list):
        return tags
    if tags:
        return [tags]

    title = (entry.get("title") or "").lower()
    summary = (entry.get("summary") or "").lower()

    if any(keyword in title or keyword in summary for keyword in ["ai", "chat", "model", "agent"]):
        return ["AI"]
    if any(keyword in title or keyword in summary for keyword in ["data", "dashboard", "chart", "analytics"]):
        return ["Data"]
    if any(keyword in title or keyword in summary for keyword in ["finance", "fintech", "invest", "financial"]):
        return ["Finance"]
    if any(keyword in title or keyword in summary for keyword in ["flask", "web", "portfolio", "website", "app"]):
        return ["Flask"]
    if any(keyword in title or keyword in summary for keyword in ["game", "gaming"]):
        return ["Games"]
    if any(keyword in title or keyword in summary for keyword in ["design", "product", "ux", "user"]):
        return ["Product Design"]
    return ["Web Development"]


@app.route("/")
def home():
    entries = load_entries()
    added = request.args.get("added") == "1"
    return render_template("index.html", entries=entries, get_entry_tags=get_entry_tags, added=added)


@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    entries = load_entries()
    if entry_id < 0 or entry_id >= len(entries):
        return "Entry not found", 404
    return render_template("entry.html", entry=entries[entry_id], entry_id=entry_id, get_entry_tags=get_entry_tags)


@app.route("/add", methods=["GET", "POST"])
def add():
    today = date.today().isoformat()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()
        learned = request.form.get("learned", "").strip()
        coolest = request.form.get("coolest", "").strip()
        entry_date = request.form.get("date", "").strip()
        screenshot = None

        if not title or not summary:
            return render_template("add.html", error="Title and summary are required.", today=today)

        # Handle file upload
        if "screenshot" in request.files:
            file = request.files["screenshot"]
            if file and file.filename and allowed_file(file.filename):
                # Create a unique filename
                filename = secure_filename(file.filename)
                timestamp = int(datetime.now().timestamp() * 1000)
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                # Store relative path for use in templates
                screenshot = f"/static/images/uploads/{filename}"
            elif file and file.filename:
                return render_template("add.html", error="Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).", today=today)

        entries = load_entries()
        entries.append({
            "title": title,
            "date": entry_date,
            "summary": summary,
            "learned": learned,
            "coolest": coolest,
            "screenshot": screenshot
        })
        save_entries(entries)
        return redirect(url_for("home", added=1))

    return render_template("add.html", error=None, today=today)


@app.route("/edit/<int:entry_id>", methods=["GET", "POST"])
def edit(entry_id):
    entries = load_entries()
    if entry_id < 0 or entry_id >= len(entries):
        return "Entry not found", 404

    entry = entries[entry_id]
    today = date.today().isoformat()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()
        learned = request.form.get("learned", "").strip()
        coolest = request.form.get("coolest", "").strip()
        entry_date = request.form.get("date", "").strip()

        if not title or not summary:
            return render_template("edit.html", entry=entry, entry_id=entry_id, error="Title and summary are required.", today=today)

        # Handle file upload
        screenshot = entry.get("screenshot")  # Keep existing screenshot by default
        if "screenshot" in request.files:
            file = request.files["screenshot"]
            if file and file.filename and allowed_file(file.filename):
                # Create a unique filename
                filename = secure_filename(file.filename)
                timestamp = int(datetime.now().timestamp() * 1000)
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                screenshot = f"/static/images/uploads/{filename}"
            elif file and file.filename:
                return render_template("edit.html", entry=entry, entry_id=entry_id, error="Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).", today=today)

        entries[entry_id] = {
            "title": title,
            "date": entry_date,
            "summary": summary,
            "learned": learned,
            "coolest": coolest,
            "screenshot": screenshot
        }
        save_entries(entries)
        return redirect(url_for("entry", entry_id=entry_id))

    return render_template("edit.html", entry=entry, entry_id=entry_id, error=None, today=today)


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete(entry_id):
    entries = load_entries()
    if entry_id < 0 or entry_id >= len(entries):
        return "Entry not found", 404

    entries.pop(entry_id)
    save_entries(entries)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)