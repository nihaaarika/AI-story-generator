<div align="center">

# 🌿 Smart Cultural Storyteller

> *"Every village has a story. Every story has a soul."*

</div>

---

## 📖 About

**Smart Cultural Storyteller** is an AI-powered web application that preserves and generates authentic folk narratives rooted in **Rural India** — inspired by the tradition of village elders sharing wisdom under a banyan tree.

Users can discover stories from a curated cultural database, or generate entirely new narratives using AI with control over mood, length, and theme. The platform blends modern generative AI with cultural sensitivity to keep India's oral storytelling traditions alive for the next generation.

> Inspired by Google's Rural India Storytelling initiative and AI Dungeon.

---

## ✨ Features

| Feature | Status |
|---|---|
| 🔍 **Story Discovery** — Search a curated database of authentic Indian folk tales | ✅ Live |
| ✨ **AI Story Generation** — Generate new stories by mood, theme & length | ✅ Live |
| 🌏 **Cultural Context** — All stories rooted in Rural Indian village life & values | ✅ Live |
| 📱 **Responsive UI** — Works on desktop and mobile | ✅ Live |
| 🎨 **AI Illustrations** — Generate scene images via Stable Diffusion | 🔧 In Progress |
| 🎵 **Audio Narration** — Text-to-speech with emotional tone (Coqui TTS) | 🔧 In Progress |
| 🌐 **Multilingual** — Hindi / English story output | 🔧 In Progress |
| 📖 **Choose Your Adventure** — Interactive branching story paths | 🗓️ Planned |

---

## 🎬 Demo

> 📸 *Screenshot / GIF coming soon — deploy in progress*

To run locally and see it yourself, follow the Quick Start below.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/nihaaarika/AI-story-generator.git
cd AI-story-generator
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example file
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
HF_TOKEN=your_huggingface_token_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 5. Load the story database

```bash
python scripts/ingest.py
```

### 6. Launch the app

```bash
python gradio_app.py
```

Then open your browser at **http://localhost:7860** 🎉

---

## 📁 Project Structure

```
AI-story-generator/
│
├── core/                       # Backend AI engines
│   ├── __init__.py
│   ├── story_engine.py         # Core story generation logic
│   ├── llm_chain.py            # LangChain LLM setup & prompting
│   ├── image_engine.py         # Stable Diffusion image generation
│   ├── audio_engine.py         # Coqui TTS audio narration
│   ├── translator.py           # Multilingual translation
│   └── session.py              # User session management
│
├── data/
│   └── stories.json            # Curated cultural story database
│
├── scripts/
│   └── ingest.py               # Load & index stories
│
├── gradio_app.py               # Main UI application (Gradio)
├── app.py                      # Entry point / app config
├── test_story.py               # Unit tests
│
├── .env.example                # Environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

```
User Input (mood + theme + length)
        ↓
   LangChain Prompt
        ↓
   OpenAI GPT-3.5
        ↓
  Cultural Story Text
        ↓
  ┌─────┴──────┐
  │            │
Image Gen   Audio TTS
(Optional) (Optional)
  │            │
  └─────┬──────┘
        ↓
  Gradio UI Display
```

The prompt is carefully engineered to ground every generated story in authentic Rural Indian culture — farming cycles, monsoon seasons, village festivals, family bonds, and elder wisdom.

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | Powers story generation via GPT |
| `HF_TOKEN` | ⚠️ Optional | Required for image generation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | [Gradio 4.0](https://gradio.app/) |
| **LLM** | OpenAI GPT-3.5-turbo via [LangChain](https://langchain.com/) |
| **Image Gen** | Stable Diffusion via HuggingFace Diffusers |
| **TTS** | Coqui TTS |
| **Translation** | HuggingFace Transformers |
| **Data** | JSON story database |
| **Deployment** | HuggingFace Spaces |

---

## 🗓️ Roadmap

- [x] Core story generation with cultural prompting
- [x] Story discovery (search curated database)
- [x] Mood / length / theme controls
- [x] Gradio UI with earthy Rural India design
- [ ] AI scene illustrations (Stable Diffusion)
- [ ] Emotional audio narration (Coqui TTS)
- [ ] Hindi language output
- [ ] Export story as PDF
- [ ] Choose-your-own-adventure branching
- [ ] HuggingFace Spaces deployment
- [ ] User story submission / community contributions

---

## 🌐 Deployment to HuggingFace Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
   - SDK: **Gradio**
   - Hardware: CPU Basic (free) or GPU for image gen
2. In your Space settings → **Secrets** → add `OPENAI_API_KEY` and `HF_TOKEN`
3. Push your code:

```bash
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/smart-cultural-storyteller
git push space main
```

---

## 🧪 Running Tests

```bash
python -m pytest test_story.py -v
```

---

## 🤝 Contributing

Contributions are welcome, especially:
- Adding more stories to `data/stories.json`
- Improving cultural accuracy of prompts
- Adding new regional Indian languages
- UI/UX improvements

```bash
# Fork → Clone → Create branch → PR
git checkout -b feature/your-feature-name
```

Please ensure no API keys or secrets are committed. See `.env.example` for the correct pattern.

---

## ⚖️ Ethics & Cultural Sensitivity

- AI-generated stories may contain inaccuracies — always verify cultural details
- Story sources are credited in `data/stories.json`
- No user data is stored or logged
- The platform aims to **celebrate** rural Indian heritage, not stereotype it

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- Inspired by **Google's Rural India Storytelling** initiative
- Built with [Gradio](https://gradio.app/), [LangChain](https://langchain.com/), and [OpenAI](https://openai.com/)
- Cultural stories sourced with respect and gratitude to India's oral tradition

---

<div align="center">

Made with ❤️ to preserve the stories of Rural India

⭐ If you find this project valuable, please give it a star!

</div>
- Verify cultural accuracy; AI may hallucinate.
- Sources credited in stories.json.
- No user data stored.

Inspired by Google's Rural India Storytelling, AI Dungeon.
