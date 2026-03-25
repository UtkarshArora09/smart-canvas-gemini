# 🖐️ Smart Canvas + Gemini Assistant

> Draw math equations in the air with your finger — let AI solve them instantly.

A real-time gesture-based drawing app that uses your **webcam + hand tracking** to let you write math equations in the air, then sends them to **Google Gemini AI** to solve.

---

## ✨ Features

- ✏️ **Air Drawing** — Draw with just your index finger using your webcam
- 🧹 **Gesture Erase** — Wipe the canvas clean with a thumb gesture
- 🤖 **AI Math Solver** — Send your handwritten equation to Gemini with a 3-finger gesture
- ⏱️ **Cooldown Timer** — Visual progress bar shows when the next AI call is ready
- 📊 **Live Answer Panel** — Gemini's step-by-step solution displayed in real time

---

## 🖼️ Demo

```
┌─────────────────────────────┬──────────────────┐
│                             │  Gemini Answer   │
│   [webcam feed]             │  ─────────────── │
│                             │  5 + 1 = 6       │
│      5 + 1  ← drawn         │                  │
│             in air          │  Add 5 and 1     │
│                             │  to get 6.       │
│  [cooldown bar at top]      │                  │
│                             │  Gestures:       │
│                             │  Index → Draw    │
│                             │  Thumb → Erase   │
│                             │  3 fingers → AI  │
└─────────────────────────────┴──────────────────┘
```

---

## 🤌 Gesture Controls

| Gesture | Action |
|---------|--------|
| ☝️ Index finger up | Draw on canvas |
| 👍 Thumb up | Erase entire canvas |
| 🤟 Index + Middle + Ring up | Send to Gemini AI |
| `Q` key | Quit |

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/smart-canvas-gemini.git
cd smart-canvas-gemini
```

### 2. Install dependencies

```bash
pip install opencv-python cvzone mediapipe google-generativeai pillow python-dotenv
```

### 3. Get a free Gemini API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **"Create API key"**
3. Copy your key

### 4. Create a `.env` file

```bash
# Create .env in the project root
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Make sure the file is named `.env` (not `_env`)

### 5. Run

```bash
python main.py
```

---

## 📦 Requirements

| Package | Purpose |
|---------|---------|
| `opencv-python` | Webcam capture & drawing |
| `cvzone` | Hand detection module |
| `mediapipe` | Hand landmark tracking |
| `google-generativeai` | Gemini API client |
| `Pillow` | Image conversion for API |
| `python-dotenv` | Load `.env` API key |

---

## 🔑 Gemini Free Tier Limits

This app uses `gemini-2.5-flash-lite` — the model with the **highest free quota**.

| Model | Requests/min | Requests/day |
|-------|-------------|--------------|
| `gemini-2.5-flash-lite` ✅ | 15 RPM | 1,000 RPD |
| `gemini-1.5-flash` | 15 RPM | 1,500 RPD |

> The app enforces a **60-second cooldown** between calls to stay safely within free tier limits.
> Daily quotas reset at **midnight Pacific Time**.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cannot open webcam` | Check camera is connected; try `cv2.VideoCapture(1)` |
| `429 Quota exceeded` | Wait for midnight PT reset, or create a new API key at [aistudio.google.com](https://aistudio.google.com) |
| `No hand detected` | Improve lighting; keep hand fully in frame |
| Drawing feels choppy | Slow down finger movement; ensure good lighting |
| `.env` not loading | Make sure file is named `.env`, not `_env` or `.env.txt` |

---

## 🗂️ Project Structure

```
smart-canvas-gemini/
├── main.py          # Main application
├── .env             # API key (not committed)
├── .gitignore       # Ignores .env and cache
└── README.md        # This file
```

---

## 🛣️ Roadmap

- [ ] Support for multiple hands
- [ ] Save drawing as image
- [ ] Support non-math questions (geometry, physics)
- [ ] Voice output for answers
- [ ] UI themes (dark/light)

---

## 📄 License

MIT License — free to use and modify.

---

> Built with OpenCV, CVZone, and Google Gemini AI ✨
