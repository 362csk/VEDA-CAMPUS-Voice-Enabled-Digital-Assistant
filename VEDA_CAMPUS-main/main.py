# main.py — VEDA-CAMPUS Entry Point
# Author: Chaithanya Sai Krishna

import sys

from modules.veda_core import ask_veda
from modules.logger import log_interaction

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def intro():
    print("\n====================================")
    print("     Welcome to VEDA CAMPUS AI      ")
    print("   Your Intelligent College Buddy   ")
    print("====================================")
    print("Ask me about syllabus, faculty, timetable, library, or materials.")
    print("Type 'exit' or 'quit' to end the session.\n")

if __name__ == "__main__":
    intro()

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "shutdown"]:
                print("VEDA > Logging off. Study well, rise high! 🚀")
                break

            response = ask_veda(user_input)
            log_interaction("TEXT", user_input, response)

            print("VEDA >", response)
        except KeyboardInterrupt:
            print("\nVEDA > Session interrupted. Goodbye! ✋")
            break
        except Exception as e:
            print(f"VEDA > ⚠️ Something went wrong: {str(e)}")

