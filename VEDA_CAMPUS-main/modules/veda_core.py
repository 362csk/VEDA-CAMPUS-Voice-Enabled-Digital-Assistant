from modules.nlu_engine import extract_intent
from modules.syllabus_query import get_syllabus
from modules.faculty_search import find_faculty
from modules.timetable_ai import get_timetable

def ask_veda(query):
    if not query or not query.strip():
        return "Please enter a question about a subject, faculty member, syllabus, or timetable."

    intent_data = extract_intent(query)
    intent = intent_data["intent"]

    if intent == "greeting":
        return "Hi! I'm VEDA, your campus assistant. Ask me about syllabus, faculty, timetable, or library."

    if intent == "exit":
        return "Goodbye! Study well, rise high."

    if intent == "syllabus":
        return get_syllabus(query)

    if intent == "faculty":
        return find_faculty(query, intent_data["topic"])

    if intent == "timetable":
        return get_timetable(query, intent_data["branch"], intent_data["day"])

    if intent == "library":
        from modules.library_ai import search_books
        return search_books(query)

    if intent == "materials":
        return "Course materials are not available in the current data. Try asking about faculty, syllabus, or timetable."

    return (
        "I couldn't identify that request. Try: "
        "'3rd year ECE syllabus', 'Who teaches DSP?', or 'CSE timetable on Monday'."
    )
