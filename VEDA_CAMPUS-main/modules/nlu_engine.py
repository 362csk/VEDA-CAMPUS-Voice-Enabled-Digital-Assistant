import csv
import json
import re
from pathlib import Path
from difflib import SequenceMatcher


DATA_DIR = Path(__file__).resolve().parents[1] / "data"

SUBJECT_ALIASES = {
    "dsp": "Digital Signal Processing",
    "d s p": "Digital Signal Processing",
    "microprocessor": "Microprocessors",
    "data structure": "Data Structures",
    "signal and system": "Signals and Systems",
    "python": "Python Programming",
}

BRANCH_ALIASES = {
    "ece": "ECE",
    "cse": "CSE",
    "cs": "CSE",
    "bca": "CSE",
    "eee": "EEE",
    "mech": "MECH",
    "mechanical": "MECH",
    "civil": "CIVIL",
}

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def _normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _load_subjects():
    subjects = set()
    syllabus_path = DATA_DIR / "syllabus.csv"
    with syllabus_path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            subject = row.get("Subject", "").strip()
            if subject:
                subjects.add(subject)

    with (DATA_DIR / "faculty.json").open(encoding="utf-8") as file:
        for faculty in json.load(file):
            subject = faculty.get("subject", "").strip()
            if subject:
                subjects.add(subject)

    timetable_path = DATA_DIR / "time_table.json"
    if timetable_path.exists():
        with timetable_path.open(encoding="utf-8") as file:
            timetable = json.load(file)
        for week in timetable.values():
            for classes in week.values():
                for item in classes:
                    subject = item.get("subject", "").strip()
                    if subject:
                        subjects.add(subject)
    return sorted(subjects, key=len, reverse=True)


KNOWN_SUBJECTS = _load_subjects()


def extract_topic(query):
    normalized_query = _normalize(query)
    if not normalized_query:
        return None

    for alias, subject in sorted(SUBJECT_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(r"\b" + re.escape(_normalize(alias)) + r"\b", normalized_query):
            return subject

    for subject in KNOWN_SUBJECTS:
        normalized_subject = _normalize(subject)
        if re.search(r"\b" + re.escape(normalized_subject) + r"\b", normalized_query):
            return subject

    query_words = [word for word in normalized_query.split() if len(word) >= 5]
    for subject in KNOWN_SUBJECTS:
        subject_words = _normalize(subject).split()
        if any(
            len(word) >= 5 and SequenceMatcher(None, word, subject_word).ratio() >= 0.86
            for word in query_words
            for subject_word in subject_words
        ):
            return subject
    return None


def _extract_year(query):
    normalized = _normalize(query)
    for pattern, year in (
        (r"\b(?:1st|first|1)(?:\s+year)?\b", "1"),
        (r"\b(?:2nd|second|2)(?:\s+year)?\b", "2"),
        (r"\b(?:3rd|third|3)(?:\s+year)?\b", "3"),
        (r"\b(?:4th|fourth|4)(?:\s+year)?\b", "4"),
    ):
        if re.search(pattern, normalized):
            return year
    return None


def _extract_branch(query):
    words = set(_normalize(query).split())
    for alias, branch in BRANCH_ALIASES.items():
        if alias in words:
            return branch
    return None


def extract_day(query):
    words = set(_normalize(query).split())
    for day in DAYS:
        if day in words:
            return day.capitalize()
    return None


def extract_intent(query):
    normalized = _normalize(query)
    words = set(normalized.split())
    year = _extract_year(query)
    branch = _extract_branch(query)
    day = extract_day(query)
    topic = extract_topic(query)

    if re.fullmatch(r"(?:please )?(?:exit|quit|shutdown|bye|stop now)(?: veda)?", normalized):
        intent = "exit"
    elif re.fullmatch(r"(?:hi|hello|hey|namaste|yo)(?: veda)?", normalized):
        intent = "greeting"
    elif "syllabus" in words or "subjects" in words:
        intent = "syllabus"
    elif words.intersection({"faculty", "teacher", "teachers", "professor", "professors", "teaches", "lecturer"}):
        intent = "faculty"
    elif words.intersection({"timetable", "schedule"}) or "time table" in normalized or "classes on" in normalized:
        intent = "timetable"
    elif words.intersection({"library", "book", "books", "reference"}):
        intent = "library"
    elif words.intersection({"materials", "notes", "pdf", "slides"}):
        intent = "materials"
    elif topic:
        intent = "faculty"
    else:
        intent = None

    return {
        "intent": intent,
        "year": year,
        "branch": branch,
        "topic": topic,
        "day": day,
    }
