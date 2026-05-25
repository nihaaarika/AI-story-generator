"""
core/story_engine.py
Handles AI story generation using Groq (free), OpenAI, or Anthropic.
No HuggingFace models needed.
"""

import os
import re
from dotenv import load_dotenv

load_dotenv()


class StoryEngine:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "groq")
        self._init_client()

    def _init_client(self):
        if self.provider == "groq":
            from groq import Groq
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = "llama-3.3-70b-versatile"

        elif self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-3.5-turbo"

        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-haiku-4-5-20251001"

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def set_provider(self, provider: str):
        self.provider = provider
        self._init_client()

    def _build_story_prompt(self, region, theme, mood, length, extra) -> str:
        extra_section = f"\nAdditional details: {extra}" if extra.strip() else ""
        return f"""You are a master storyteller of Rural India. Write an authentic folk story.

STORY PARAMETERS:
- Region: {region}
- Theme: {theme}
- Mood: {mood}
- Target length: {length}
{extra_section}

REQUIREMENTS:
1. Open with a vivid scene set in {region}
2. Use culturally authentic details: seasons, customs, village life, nature
3. Include a memorable character with a local name
4. Write like an oral tale told by an elder
5. End with a resonant closing line
6. NO headers — continuous narrative paragraphs only
7. Do NOT write a title as the first line

After the story, on a new line write:
TITLE: [a poetic 4-7 word title]
IMAGE_PROMPT: [20-word visual description for illustration, no faces, painterly]"""

    def _build_continue_prompt(self, existing, region, theme, mood) -> str:
        snippet = existing[-800:] if len(existing) > 800 else existing
        return f"""Continue this Rural Indian folk story naturally for 200-300 more words:

\"\"\"{snippet}\"\"\"

Maintain the same voice, tone, region ({region}), theme ({theme}), mood ({mood}).

After the continuation write:
TITLE: [updated title]
IMAGE_PROMPT: [20-word visual scene prompt, no faces]"""

    def _call_llm(self, prompt: str) -> str:
        if self.provider in ("groq", "openai"):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1400,
                temperature=0.88,
            )
            return response.choices[0].message.content

        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1400,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text

    def _parse_output(self, raw: str) -> tuple:
        title_match = re.search(r"TITLE:\s*(.+)", raw)
        image_match = re.search(r"IMAGE_PROMPT:\s*(.+)", raw)

        title = title_match.group(1).strip() if title_match else "A Story from Rural India"
        image_prompt = image_match.group(1).strip() if image_match else "rural India village scene, watercolour"

        body = re.sub(r"\nTITLE:.*", "", raw)
        body = re.sub(r"\nIMAGE_PROMPT:.*", "", body).strip()

        return title, body, image_prompt

    def generate(self, region, theme, mood, length, extra="") -> tuple:
        prompt = self._build_story_prompt(region, theme, mood, length, extra)
        raw = self._call_llm(prompt)
        return self._parse_output(raw)

    def continue_story(self, existing, region, theme, mood) -> tuple:
        prompt = self._build_continue_prompt(existing, region, theme, mood)
        raw = self._call_llm(prompt)
        return self._parse_output(raw)