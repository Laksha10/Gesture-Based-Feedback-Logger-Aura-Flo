# 🧘 Gesture-Based Feedback Logger – Aura Flo

> MediaPipe · Whisper-Tiny · SQLite · VADER · Raspberry Pi

A gesture-triggered feedback logging system designed for wellness sessions (e.g., yoga, physiotherapy) on resource-constrained devices like the Raspberry Pi. Combines pose detection, offline voice transcription, and NLP-based sentiment tagging to capture in-the-moment physical and emotional states.

---

## 🛠 Features

- ✋ **Gesture Activation**: Detects specific pose (e.g., hands on heart) via **MediaPipe**
- 🎤 **Voice Feedback**: Activates **Whisper-Tiny** offline model to transcribe voice
- 💾 **Local Storage**: Saves feedback + timestamp + pose + sentiment into **SQLite**
- 🧠 **Sentiment Analysis**: Classifies feedback as positive / negative / pain-related via **VADER**
- 📊 **Dashboard View**: Displays scrolling summary of logs alongside session video

---

## 📦 Tech Stack

| Component        | Tool / Model        |
|------------------|---------------------|
| Pose Detection   | MediaPipe (Pose)    |
| Audio Transcription | Whisper-Tiny (offline) |
| Sentiment Analysis | VADER Sentiment    |
| Local Storage    | SQLite3             |
| Device           | Raspberry Pi (optimized) |

