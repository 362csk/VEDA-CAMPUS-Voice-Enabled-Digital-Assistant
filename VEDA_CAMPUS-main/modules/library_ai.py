import json
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "books.json"


def search_library(query):
    if not DATA_PATH.exists():
        return "Library data not found."

    try:
        with DATA_PATH.open(encoding="utf-8") as file:
            books = json.load(file)
    except json.JSONDecodeError as error:
        return f"Library data is invalid: {error}"

    ignored_words = {"a", "about", "and", "book", "books", "find", "for", "i", "in", "library", "me", "of", "the", "show"}
    keywords = {
        word for word in re.findall(r"[a-z0-9]+", query.lower())
        if word not in ignored_words
    }
    matches = []

    for book in books:
        searchable_text = " ".join(
            [book.get("title", ""), book.get("author", "")]
            + book.get("topics", [])
        ).lower()
        book_words = set(re.findall(r"[a-z0-9]+", searchable_text))
        if keywords & book_words:
            info = (
                f"📘 {book.get('title', 'Unknown title')} by {book.get('author', 'Unknown author')}\n"
                f"  • QR Code: {book.get('qr', 'Not listed')}\n"
                f"  • Rack: {book.get('rack', 'Not listed')}\n"
                f"  • Topics: {', '.join(book.get('topics', []))}"
            )
            matches.append(info)

    if matches:
        return "\n\n".join(matches)
    return "No relevant books found. Try a subject or topic such as signals, Fourier, 8085, or modulation."


def search_books(query):
    return search_library(query)
