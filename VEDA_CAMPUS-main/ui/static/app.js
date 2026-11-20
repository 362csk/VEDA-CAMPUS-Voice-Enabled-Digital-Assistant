const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const welcome = document.querySelector("#welcome-block");
const typing = document.querySelector("#typing-indicator");
const sendButton = document.querySelector("#send-button");
const micButton = document.querySelector("#mic-button");
const voiceToggle = document.querySelector("#voice-toggle");
const voiceStatus = document.querySelector("#voice-status");
const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let voiceReplies = false;

if (!SpeechRecognitionAPI) {
  micButton.disabled = true;
  micButton.title = "Voice input is not supported by this browser";
  voiceStatus.textContent = "Voice input is not supported by this browser.";
}

if (!("speechSynthesis" in window)) {
  voiceToggle.disabled = true;
  voiceToggle.title = "Spoken replies are not supported by this browser";
}

function scrollToLatest() {
  const conversation = document.querySelector(".conversation");
  conversation.scrollTop = conversation.scrollHeight;
}

function addMessage(role, text) {
  const message = document.createElement("article");
  message.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "user" ? "Y" : "V";

  const content = document.createElement("div");
  content.className = "message-content";

  const label = document.createElement("span");
  label.className = "message-label";
  label.textContent = role === "user" ? "YOU" : "VEDA";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = text;

  content.append(label, bubble);
  message.append(avatar, content);
  messages.append(message);
  welcome.hidden = true;
  scrollToLatest();
}

function speakReply(text) {
  if (!voiceReplies || !("speechSynthesis" in window)) return;

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = navigator.language || "en-US";
  window.speechSynthesis.speak(utterance);
}

function startVoiceInput() {
  if (!SpeechRecognitionAPI) return;

  if (recognition) {
    recognition.stop();
    return;
  }

  const activeRecognition = new SpeechRecognitionAPI();
  recognition = activeRecognition;
  activeRecognition.lang = navigator.language || "en-US";
  activeRecognition.continuous = false;
  activeRecognition.interimResults = false;

  activeRecognition.onstart = () => {
    micButton.classList.add("listening");
    micButton.setAttribute("aria-label", "Stop voice input");
    micButton.title = "Stop listening";
    voiceStatus.textContent = "Listening… speak now.";
  };

  activeRecognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map((result) => result[0].transcript)
      .join(" ")
      .trim();

    if (transcript) {
      voiceStatus.textContent = `Heard: ${transcript}`;
      sendMessage(transcript);
    } else {
      voiceStatus.textContent = "No speech was recognized. Try again.";
    }
  };

  activeRecognition.onerror = (event) => {
    const messages = {
      "not-allowed": "Allow microphone access in your browser settings.",
      "service-not-allowed": "The browser speech service is unavailable.",
      "no-speech": "No speech detected. Click the microphone and try again.",
      network: "Voice recognition needs an available network service.",
    };
    voiceStatus.textContent = messages[event.error] || `Voice input error: ${event.error}.`;
  };

  activeRecognition.onend = () => {
    if (recognition === activeRecognition) recognition = null;
    micButton.classList.remove("listening");
    micButton.setAttribute("aria-label", "Speak your message");
    micButton.title = "Speak your message";
    if (voiceStatus.textContent === "Listening… speak now.") {
      voiceStatus.textContent = "Microphone ready.";
    }
  };

  try {
    activeRecognition.start();
  } catch (error) {
    recognition = null;
    voiceStatus.textContent = `Could not start voice input: ${error.message}`;
  }
}

async function sendMessage(message) {
  const trimmed = message.trim();
  if (!trimmed || sendButton.disabled) return;

  addMessage("user", trimmed);
  input.value = "";
  input.style.height = "auto";
  typing.classList.add("visible");
  typing.setAttribute("aria-hidden", "false");
  sendButton.disabled = true;
  micButton.disabled = true;
  scrollToLatest();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: trimmed }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "VEDA could not answer right now.");
    addMessage("assistant", result.reply);
    speakReply(result.reply);
  } catch (error) {
    addMessage("assistant", `I couldn't reach the chat service. ${error.message}`);
  } finally {
    typing.classList.remove("visible");
    typing.setAttribute("aria-hidden", "true");
    sendButton.disabled = false;
    micButton.disabled = !SpeechRecognitionAPI;
    input.focus();
    scrollToLatest();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 125)}px`;
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
    event.preventDefault();
    form.requestSubmit();
  }
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.prompt));
});

document.querySelector("#clear-chat").addEventListener("click", () => {
  messages.replaceChildren();
  welcome.hidden = false;
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
  input.focus();
});

micButton.addEventListener("click", startVoiceInput);

voiceToggle.addEventListener("click", () => {
  voiceReplies = !voiceReplies;
  voiceToggle.setAttribute("aria-pressed", String(voiceReplies));
  voiceToggle.textContent = voiceReplies ? "🔊 Voice replies: on" : "🔊 Voice replies: off";
  voiceStatus.textContent = voiceReplies
    ? "VEDA will speak its replies."
    : "Spoken replies are off.";
  if (!voiceReplies && "speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
});

async function loadSubjects() {
  const subjectList = document.querySelector("#subject-list");
  try {
    const response = await fetch("/api/subjects");
    if (!response.ok) throw new Error("Unable to load subjects.");
    const subjects = await response.json();
    document.querySelector("#subject-count").textContent = subjects.length;
    subjectList.replaceChildren();
    subjects.slice(0, 12).forEach((subject) => {
      const chip = document.createElement("span");
      chip.className = "subject-chip";
      chip.textContent = subject;
      subjectList.append(chip);
    });
  } catch {
    subjectList.textContent = "Subjects are unavailable.";
  }
}

async function loadFaculty() {
  const facultyList = document.querySelector("#faculty-list");
  try {
    const response = await fetch("/api/faculty");
    if (!response.ok) throw new Error("Unable to load faculty.");
    const faculty = await response.json();
    document.querySelector("#faculty-count").textContent = faculty.length;
    facultyList.replaceChildren();
    faculty.forEach((person) => {
      const card = document.createElement("div");
      card.className = "faculty-card";

      const avatar = document.createElement("span");
      avatar.className = "faculty-avatar";
      avatar.textContent = person.name
        .split(/\s+/)
        .filter((part) => !["Dr.", "Mr.", "Ms.", "Mrs.", "Prof."].includes(part))
        .slice(0, 2)
        .map((part) => part[0])
        .join("")
        .toUpperCase();

      const details = document.createElement("div");
      const name = document.createElement("strong");
      name.textContent = person.name;
      if (person.demo) {
        const demo = document.createElement("span");
        demo.className = "demo-tag";
        demo.textContent = "DEMO";
        name.append(demo);
      }
      const subject = document.createElement("small");
      subject.textContent = `${person.department} · ${person.subject}`;

      details.append(name, subject);
      card.append(avatar, details);
      facultyList.append(card);
    });
  } catch {
    facultyList.textContent = "Faculty data is unavailable.";
  }
}

loadSubjects();
loadFaculty();
input.focus();
