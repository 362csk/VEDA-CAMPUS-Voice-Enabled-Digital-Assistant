import json
import os
import re

# Absolute path to data/faculty.json
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "faculty.json")


def get_faculty_directory():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Faculty database not found: {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def find_faculty(query, topic=None):
    try:
        data = get_faculty_directory()
        normalized_query = re.sub(r"[^a-z0-9]+", " ", query.lower()).strip()
        matches = []

        for faculty in data:
            name = faculty.get("name", "")
            subject = faculty.get("subject", "")
            department = faculty.get("department", "")
            normalized_subject = re.sub(r"[^a-z0-9]+", " ", subject.lower()).strip()
            normalized_name = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
            subject_requested = topic and normalized_subject == re.sub(
                r"[^a-z0-9]+", " ", topic.lower()
            ).strip()
            query_has_subject = normalized_subject and re.search(
                r"\b" + re.escape(normalized_subject) + r"\b", normalized_query
            )
            query_has_department = department.lower() in normalized_query.split()
            query_has_name = normalized_name and normalized_name in normalized_query

            if subject_requested or query_has_subject or query_has_department or query_has_name:
                demo_label = " [DEMO RECORD]" if faculty.get("demo") else ""
                info = (
                    f"👨‍🏫 {name}{demo_label} ({department})\n"
                    f"  • Subject: {subject}\n"
                    f"  • Email: {faculty.get('email', 'Not listed')}\n"
                    f"  • Room: {faculty.get('room', 'Not listed')}"
                )
                matches.append(info)

        if matches:
            return "\n\n".join(matches)
        else:
            return "🔍 No matching faculty found. Try using subject or department name."

    except (OSError, json.JSONDecodeError) as e:
        return f"❌ Error in faculty search: {str(e)}"
