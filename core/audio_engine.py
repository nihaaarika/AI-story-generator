"""
core/audio_engine.py
Converts story text to spoken audio narration.
Uses gTTS (Google Text-to-Speech) — free, no API key needed.
Optional: pyttsx3 for offline fallback.
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("generated_audio")
OUTPUT_DIR.mkdir(exist_ok=True)


class AudioEngine:
    def __init__(self):
        self.speed  = float(os.getenv("TTS_SPEED", "0.9"))
        self.lang   = os.getenv("TTS_LANG", "en")
        self.backend = self._detect_backend()

    def _detect_backend(self) -> str:
        """Auto-detect the best available TTS backend."""
        try:
            import gtts  # noqa
            return "gtts"
        except ImportError:
            pass
        try:
            import pyttsx3  # noqa
            return "pyttsx3"
        except ImportError:
            pass
        return "none"

    def set_speed(self, speed: float):
        self.speed = speed

    def set_language(self, lang: str):
        self.lang = lang

    # ── gTTS backend (recommended) ────────────────────────────────────────────
    def _narrate_gtts(self, text: str, filename: str) -> str:
        from gtts import gTTS
        from gtts.tts import gTTSError

        # gTTS doesn't have a speed param directly — use slow=True for slower pace
        slow = self.speed < 0.85
        tts = gTTS(text=text, lang=self.lang, slow=slow)
        tts.save(filename)
        return filename

    # ── pyttsx3 backend (offline fallback) ────────────────────────────────────
    def _narrate_pyttsx3(self, text: str, filename: str) -> str:
        import pyttsx3
        engine = pyttsx3.init()
        rate = engine.getProperty("rate")
        engine.setProperty("rate", int(rate * self.speed))
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename

    # ── Public API ────────────────────────────────────────────────────────────
    def narrate(self, title: str, story_body: str) -> str | None:
        """
        Convert story to audio file.
        Returns: local file path (.mp3), or None if TTS unavailable.
        """
        if self.backend == "none":
            print("[AudioEngine] No TTS backend installed. "
                  "Run: pip install gtts")
            return None

        # Build narration text: title pause then story
        full_text = f"{title}. ... {story_body}"

        seed = int(time.time()) % 99999
        filename = str(OUTPUT_DIR / f"narration_{seed}.mp3")

        try:
            if self.backend == "gtts":
                return self._narrate_gtts(full_text, filename)
            elif self.backend == "pyttsx3":
                return self._narrate_pyttsx3(full_text, filename)
        except Exception as e:
            print(f"[AudioEngine] Narration failed: {e}")
            return None