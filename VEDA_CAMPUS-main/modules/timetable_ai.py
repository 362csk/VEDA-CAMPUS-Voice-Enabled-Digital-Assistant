import json
import re
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "time_table.json"


def _find_branch(query):
    normalized = re.sub(r"[^a-z0-9]+", " ", query.lower()).split()
    aliases = {
        "ece": "ECE",
        "cse": "CSE",
        "cs": "CSE",
        "bca": "CSE",
        "eee": "EEE",
        "mech": "MECH",
        "civil": "CIVIL",
    }
    return next((branch for alias, branch in aliases.items() if alias in normalized), None)


def get_timetable(query, branch=None, day=None):
    if not DATA_PATH.exists():
        return "📂 Timetable data file not found."

    try:
        with DATA_PATH.open(encoding="utf-8") as file:
            timetables = json.load(file)
    except json.JSONDecodeError as error:
        return f"❌ Timetable data is invalid: {error}"

    branch = branch or _find_branch(query)
    if not branch:
        available = ", ".join(sorted(timetables))
        return f"Please specify a department. Timetables are available for: {available}."

    week = timetables.get(branch.upper())
    if week is None:
        available = ", ".join(sorted(timetables))
        return f"No timetable is available for {branch.upper()}. Available departments: {available}."

    days = [day.capitalize()] if day else list(week)
    sections = []
    for selected_day in days:
        classes = week.get(selected_day)
        if classes is None:
            sections.append(f"{selected_day}: no timetable data available.")
            continue
        entries = [
            f"  • {item['time']}: {item['subject']}"
            for item in classes
        ]
        sections.append(f"{selected_day}\n" + "\n".join(entries))

    return f"📆 {branch.upper()} timetable\n\n" + "\n\n".join(sections)
