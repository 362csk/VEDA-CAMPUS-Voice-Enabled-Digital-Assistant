# VEDA Campus Assistant

VEDA (Voice-Enabled Digital Assistant) is a Python campus-information assistant. It can answer questions using the project's local syllabus, faculty, timetable, and book data. It offers a terminal chat, a microphone-based voice assistant, and a browser-based chat website.

> **Faculty data notice:** Some entries in `data/faculty.json` are illustrative demo records. They are marked with `"demo": true`, displayed with a DEMO label, and use reserved `example.com` email addresses. Replace them with verified details before using this project as an authoritative campus directory.

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

## Requirements

- Python 3.11 is recommended (the project environment was set up with Python 3.11).
- Windows is the primary target for the voice assistant. Voice mode needs a working microphone and audio playback.
- An internet connection is required for Python voice recognition because the application uses SpeechRecognition's Google recognition service.
- Terminal chat and website text chat do not require a microphone or internet connection. Browser voice recognition may require an internet connection, depending on the browser's speech service.
- Packages in `requirements.txt` are needed for voice mode:
  - `SpeechRecognition`
  - `pyttsx3`
  - `PyAudio`

The website and terminal chat use Python's standard library. Installing `requirements.txt` also installs the voice dependencies.

## Installation (Windows PowerShell)

Open PowerShell in the project folder:

```powershell
cd "D:\Class Work\VEDA_CAMPUS-main"
```

Create and activate a virtual environment, then install the packages:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.11` is unavailable, install Python 3.11 and try `python -m venv .venv`.

If PowerShell prevents environment activation, allow it for the current PowerShell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run VEDA

Run each mode from the project root, in a separate terminal session.

### Terminal chat

```powershell
python main.py
```

Type a question at the `You >` prompt. Enter `exit`, `quit`, or `shutdown` to end the session.

### Website

Start the local web server:

```powershell
python -m ui.app
```

Open **http://127.0.0.1:8000** in a browser. Keep the terminal and server running while using the site. Press `Ctrl+C` in the server terminal to stop it.

Do not open `ui/static/index.html` directly as a `file://` URL. The website loads its subject and faculty lists and sends chat messages to the Python server's API.

The microphone button uses your browser's Web Speech API to transcribe a question and send it to VEDA. The **Voice replies** button enables or disables spoken answers using browser text-to-speech. Browser speech-recognition support varies; use a supported browser such as a recent Chrome or Edge, allow microphone access, and keep the site open at `http://127.0.0.1:8000`.

The server binds to `127.0.0.1` (this computer only). It is intended for local development, not as a publicly deployed or production server.

The website API provides:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/subjects` | Return subjects found in the project data |
| `GET` | `/api/faculty` | Return the faculty directory |
| `POST` | `/api/chat` | Answer a chat message |

Example chat request:

```json
{"message": "Who teaches DSP?"}
```

### Voice assistant

```powershell
python -m modules.voice_veda
```

You can also run the script directly:

```powershell
python modules\voice_veda.py
```

Speak after the assistant says it is listening. It calibrates for background noise, waits up to 10 seconds for speech to begin, and limits each phrase to 8 seconds. Say `exit`, `quit`, `shutdown`, `bye VEDA`, `VEDA exit`, or `stop now` to quit.

## Example questions

| You can ask | VEDA uses |
|---|---|
| `Hi` | Greeting response |
| `3rd year ECE syllabus` | Matching year and department in the syllabus CSV |
| `What subjects are in 1st year ECE?` | Syllabus data for the requested year and department |
| `Who teaches DSP?` | DSP subject alias and faculty data |
| `Who teaches Microprocessor?` | Subject lookup in the faculty directory |
| `Show me CSE faculty` | Faculty records for the CSE department |
| `CSE timetable on Monday` | CSE schedule for Monday |
| `ECE timetable` | ECE schedule for the available week |
| `Find a book about Fourier` | Book titles and topics in the local catalog |
| `Find a book about 8085` | Matching topic in the local catalog |

For syllabus questions, include both a year and a department. Timetable data is currently available for ECE and CSE. Answers are limited to information in the local data files; the assistant does not generate facts that are missing from them.

## Project data

The assistant reads these files from `data/`:

### `syllabus.csv`

CSV columns:

```text
Year,Branch,Subject,Units
```

Add one row per subject. Use year values `1` through `4` and a department code such as `ECE` or `CSE`.

### `faculty.json`

A JSON array of records:

```json
{
  "name": "Faculty Name",
  "department": "ECE",
  "subject": "Digital Signal Processing",
  "email": "faculty@example.com",
  "room": "Block A - Room 204"
}
```

The optional `"demo": true` property identifies example records. Replace demo entries with verified data or remove them. Keep the JSON valid when editing the file.

### `time_table.json`

The timetable is organized by department, day, then a list of classes:

```json
{
  "ECE": {
    "Monday": [
      {"time": "9:00 - 10:00", "subject": "Digital Signal Processing"}
    ]
  }
}
```

### `books.json`

The local book catalog is a JSON array with `title`, `author`, `topics`, `qr`, and `rack` fields. Search matches words in the title, author, or topic list.

Subject matching is built from the syllabus, faculty, and timetable files. As those files change, the website's subject list and the assistant's recognized subjects update when the application is restarted.

## Logs and privacy

Text queries and VEDA responses are written to `logs/veda_logs.txt`. Run the app from the project root so logs go to the expected `logs` folder. The project logs text interactions; it does not save microphone recordings.

Voice recognition sends captured audio to the Google recognition service through the SpeechRecognition package. Do not use voice mode for sensitive conversations.

Website voice input is handled by the browser and may use a browser-provided online recognition service. Check the browser's privacy settings and policies before using it for sensitive conversations.

## Troubleshooting

### The website cannot connect or chat says it cannot reach the service

1. Start the server from the project root with `python -m ui.app`.
2. Keep that terminal open while using the website.
3. Open or refresh `http://127.0.0.1:8000`.
4. Do not use `file://` to open the HTML file directly.
5. If port 8000 is already in use, stop the other process using it before starting VEDA.

### `No module named 'modules'`

Run the command from the project root. For the website use `python -m ui.app`; for the voice mode use `python -m modules.voice_veda`.

### The microphone is not hearing speech

- Check that Windows has the correct microphone selected and that applications are allowed to use it.
- Move to a quieter environment and speak after the “Listening...” prompt.
- Confirm the microphone works in another application.
- Confirm internet access is available for speech recognition.
- If the recognition service reports an error, try again when the service and network are available.

### The website voice button is unavailable or does not respond

- Use a browser that supports the Web Speech API; support varies by browser and version.
- Allow microphone access for `127.0.0.1` in the browser's site permissions.
- Start the website through `python -m ui.app` and use `http://127.0.0.1:8000`, rather than opening the HTML file directly.
- The microphone transcribes and submits speech. Turn on **Voice replies** separately if you want VEDA's answers spoken aloud.

### PyAudio fails to install

Use Python 3.11 in the virtual environment, upgrade pip, and retry `pip install -r requirements.txt`. PyAudio is only needed for microphone-based voice mode; the terminal and website modes do not capture audio.

### A faculty member, syllabus item, book, or timetable entry is missing

Check the corresponding JSON or CSV file in `data/`. The project contains sample data, not a complete or official campus database. For faculty details, confirm whether a record is marked as a demo entry.

### The terminal displays odd characters

Use a modern Windows Terminal or PowerShell session and run the project with its virtual environment's Python interpreter.

## Project structure

```text
VEDA_CAMPUS-main/
├── main.py
├── requirements.txt
├── data/
│   ├── books.json
│   ├── faculty.json
│   ├── syllabus.csv
│   └── time_table.json
├── modules/
│   ├── faculty_search.py
│   ├── library_ai.py
│   ├── logger.py
│   ├── nlu_engine.py
│   ├── syllabus_query.py
│   ├── timetable_ai.py
│   ├── veda_core.py
│   └── voice_veda.py
├── ui/
│   ├── app.py
│   └── static/
│       ├── app.js
│       ├── index.html
│       └── styles.css
├── assets/
└── logs/
```

## Technology

- Python 3 and standard library for the chat logic and local HTTP server
- SpeechRecognition, PyAudio, and pyttsx3 for voice mode
- HTML, CSS, and JavaScript for the website
- CSV and JSON files for the local knowledge base

## Author

Chaithanya Sai Krishna

GitHub: [github.com/362csk](https://github.com/362csk)
