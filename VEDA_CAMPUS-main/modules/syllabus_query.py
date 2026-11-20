import csv
import os
import re

# Point to project root: VEDA_CAMPUS/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "syllabus.csv")

def get_syllabus(query):
    try:
        if not os.path.exists(DATA_PATH):
            return "📂 Syllabus data file not found."

        query_lower = query.lower()
        year = None
        for pattern, value in (
            (r"\b(?:1st|first|1)(?:\s+year)?\b", "1"),
            (r"\b(?:2nd|second|2)(?:\s+year)?\b", "2"),
            (r"\b(?:3rd|third|3)(?:\s+year)?\b", "3"),
            (r"\b(?:4th|fourth|4)(?:\s+year)?\b", "4"),
        ):
            if re.search(pattern, query_lower):
                year = value
                break

        branch = None
        for candidate in ["ece", "cse", "mech", "civil", "eee"]:
            if re.search(r"\b" + candidate + r"\b", query_lower):
                branch = candidate.upper()
                break

        if not year or not branch:
            return "❓ Please specify the year and branch (e.g., '3rd year ECE syllabus')."

        results = []
        with open(DATA_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Year'].strip() == year and row['Branch'].strip().upper() == branch:
                    results.append(f"📘 {row['Subject'].strip()} – {row['Units'].strip()} units")

        if results:
            return "\n".join(results)
        else:
            return f"⚠️ No syllabus found for {year} year {branch}."

    except Exception as e:
        return f"❌ Error processing syllabus: {str(e)}"
