"""
core/image_engine.py
Generates story illustrations using Pollinations AI (free, no key needed)
or Stable Diffusion via HuggingFace Inference API (optional, needs HF_TOKEN).
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)


class ImageEngine:
    def __init__(self):
        self.style = "watercolour folk art, earthy warm tones"
        self.hf_token = os.getenv("HF_TOKEN", "")
        # Use HuggingFace if token is set, otherwise Pollinations (free)
        self.backend = "huggingface" if self.hf_token else "pollinations"

    def set_style(self, style: str):
        style_map = {
            "Watercolour folk art":    "watercolour folk art, earthy warm tones, hand-painted",
            "Madhubani painting style": "madhubani painting, bold outlines, folk patterns, traditional Indian",
            "Warli tribal art":        "warli tribal art, white on terracotta, geometric, minimalist",
            "Realistic photography":   "golden hour photography, rural India, warm natural light, DSLR",
            "Oil painting":            "oil painting, impressionist, rich textures, warm palette",
        }
        self.style = style_map.get(style, style)

    def _build_prompt(self, base_prompt: str) -> str:
        return (
            f"{base_prompt}, {self.style}, "
            "no text, no words, no letters, no watermark, "
            "highly detailed, atmospheric, beautiful composition"
        )

    # ── Pollinations AI (free, no key) ────────────────────────────────────────
    def _generate_pollinations(self, prompt: str) -> str:
        encoded = requests.utils.quote(prompt)
        seed = int(time.time()) % 99999
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=896&height=512&seed={seed}&nologo=true&enhance=true"
        )
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        filename = OUTPUT_DIR / f"story_{seed}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        return str(filename)

    # ── HuggingFace Inference API (needs HF_TOKEN) ────────────────────────────
    def _generate_huggingface(self, prompt: str) -> str:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 896, "height": 512,
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        seed = int(time.time()) % 99999
        filename = OUTPUT_DIR / f"story_{seed}.jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        return str(filename)

    # ── Public API ────────────────────────────────────────────────────────────
    def generate(self, base_prompt: str) -> str:
        """
        Generate an illustration for the story.
        Returns: local file path to the saved image.
        """
        full_prompt = self._build_prompt(base_prompt)
        try:
            if self.backend == "huggingface":
                return self._generate_huggingface(full_prompt)
            else:
                return self._generate_pollinations(full_prompt)
        except Exception as e:
            print(f"[ImageEngine] Generation failed: {e}")
            return None