# VEDA-CAMPUS-Voice-Enabled-Digital-Assistant
Developed VEDA CAMPUS, a Python-based voice and text assistant that answers student queries about syllabus, faculty, and timetables. Implemented custom NLU for intent detection, CSV/JSON-based data retrieval, speech recognition, text-to-speech, and interaction logging.
## Features

- **Terminal chat:** ask questions in `main.py`.
- **Voice chat:** speech recognition and text-to-speech through `modules/voice_veda.py`.
- **Local website:** responsive HTML, CSS, and JavaScript chat, served by a small Python HTTP server.
- **Syllabus lookup:** searches `data/syllabus.csv` using the requested year and department.
- **Faculty lookup:** searches `data/faculty.json` by subject, subject abbreviation, faculty name, or department.
- **Timetable lookup:** searches `data/time_table.json` by department and, optionally, day.
- **Book lookup:** searches titles, authors, and topics in `data/books.json`.
- **Interaction logging:** terminal, voice, and website conversations are appended to `logs/veda_logs.txt`.
- **Rule-based language understanding:** intent and subject matching use local Python logic and project data; no LLM is required.
