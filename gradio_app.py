"""
Smart Cultural Storyteller — Main Gradio Application
Run: python gradio_app.py
"""

import gradio as gr
from core.story_engine import StoryEngine
from core.image_engine import ImageEngine
from core.audio_engine import AudioEngine
from core.session import SessionManager
import os

# ── Initialise engines ──────────────────────────────────────────────────────
story_engine = StoryEngine()
image_engine = ImageEngine()
audio_engine = AudioEngine()
session_mgr  = SessionManager()

# ── Constants ────────────────────────────────────────────────────────────────
REGIONS = [
    "Rural Rajasthan",
    "Villages of Kerala",
    "Bihar countryside",
    "Punjab farmlands",
    "Tribal Odisha",
    "Himalayan foothills (Uttarakhand)",
    "Deccan plateau villages",
    "Bengal river delta",
]

THEMES = [
    "Devotion & Faith",
    "Harvest & Seasons",
    "Love & Longing",
    "Wisdom of Elders",
    "Village Festival",
    "Bravery & Sacrifice",
    "Nature Spirits & Folklore",
    "Family Bonds",
]

MOODS = [
    "Contemplative",
    "Joyful",
    "Melancholic",
    "Mystical",
    "Hopeful",
    "Bittersweet",
    "Adventurous",
    "Serene",
]

LENGTHS = {
    "Short  (~200 words)":  "200-250 words",
    "Medium (~400 words)":  "350-450 words",
    "Long   (~700 words)":  "600-750 words",
}

# ── Custom CSS ───────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,500&family=Crimson+Pro:ital,wght@0,300;0,400;0,500;1,300;1,400&display=swap');

:root {
    --ink:            #1a1208;
    --ink-mid:        #3d2e14;
    --ink-light:      #7a6245;
    --parchment:      #fdf6e3;
    --parchment-dark: #f5e9c8;
    --saffron:        #d4840a;
    --saffron-light:  #f0a832;
    --terracotta:     #b85c2a;
    --forest:         #2d5a27;
    --border:         rgba(180,130,50,0.3);
}

/* ── Page shell ── */
body, .gradio-container {
    background: var(--parchment) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
    color: var(--ink) !important;
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(212,132,10,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(184,92,42,0.05) 0%, transparent 50%) !important;
}

/* ── Banner ── */
#banner {
    background: var(--ink);
    border-bottom: 2px solid var(--saffron);
    padding: 1.2rem 2rem;
    text-align: center;
    margin-bottom: 0 !important;
}
#banner h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem !important;
    color: var(--saffron-light) !important;
    margin: 0 !important;
    font-weight: 700 !important;
}
#banner p {
    color: rgba(255,255,255,0.65) !important;
    font-size: 1rem !important;
    font-style: italic !important;
    margin: 0.3rem 0 0 !important;
    font-family: 'Crimson Pro', serif !important;
}

/* ── Tabs ── */
.tab-nav button {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--ink-light) !important;
    border-radius: 0 !important;
    padding: 0.7rem 1.8rem !important;
}
.tab-nav button.selected {
    color: var(--saffron) !important;
    border-bottom: 2px solid var(--saffron) !important;
    background: transparent !important;
}

/* ── Labels ── */
label, .label-wrap span {
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: var(--ink-mid) !important;
}

/* ── Inputs / selects ── */
input[type=text], textarea, select, .gr-input, .gr-select {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
    background: #fffdf5 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
}
input[type=text]:focus, textarea:focus {
    border-color: var(--saffron) !important;
    box-shadow: 0 0 0 3px rgba(231,132,10,0.15) !important;
}

/* ── Buttons ── */
button.primary, .gr-button-primary {
    background: var(--ink) !important;
    color: var(--saffron-light) !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s !important;
}
button.primary:hover { background: #3d2e14 !important; transform: translateY(-1px) !important; }

button.secondary, .gr-button-secondary {
    background: transparent !important;
    color: var(--ink-mid) !important;
    font-family: 'Crimson Pro', serif !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
button.secondary:hover { background: var(--parchment-dark) !important; }

/* ── Story output box ── */
#story-output-box {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.1rem !important;
    line-height: 1.85 !important;
    color: var(--ink-mid) !important;
    background: #fffdf8 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.5rem 2rem !important;
    white-space: pre-wrap !important;
}
#story-title-box {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.5rem 0 !important;
}

/* ── Status message ── */
#status-box {
    font-family: 'Crimson Pro', serif !important;
    font-style: italic !important;
    font-size: 0.95rem !important;
    color: var(--saffron) !important;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.2rem !important;
    color: var(--ink) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 1rem !important;
}

/* ── Image output ── */
#story-image img {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* ── Audio output ── */
#audio-player audio {
    width: 100% !important;
    border-radius: 8px !important;
}

/* ── Accordion ── */
.gr-accordion {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: #fffdf5 !important;
}

/* ── Discover card grid ── */
#discover-gallery .thumbnail-item {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--parchment-dark); }
::-webkit-scrollbar-thumb { background: var(--saffron); border-radius: 3px; }
"""

# ── Helper: build story metadata string ─────────────────────────────────────
def build_meta(region, theme, mood, length_label):
    return f" {region}  ·   {mood}  ·  {theme}  ·   {length_label.split('(')[0].strip()}"


# ── Core action: Generate Story ──────────────────────────────────────────────
def generate_story(region, theme, mood, length_label, extra_details, history):
    length_words = LENGTHS[length_label]

    # 1. Generate story text
    yield (
        " Writing your story…", "", "", None, None, history
    )

    try:
        title, story_body, image_prompt = story_engine.generate(
            region=region,
            theme=theme,
            mood=mood,
            length=length_words,
            extra=extra_details,
        )
    except Exception as e:
        yield (f" Story generation failed: {e}", "", "", None, None, history)
        return

    meta = build_meta(region, theme, mood, length_label)

    # 2. Save to session history
    history = session_mgr.add_story(history, title, story_body, region, theme, mood)

    yield (
        " Story ready — generating illustration…",
        title,
        f"{meta}\n\n{story_body}",
        None,
        None,
        history,
    )

    # 3. Generate image
    try:
        img_path = image_engine.generate(image_prompt)
    except Exception:
        img_path = None

    yield (
        " Preparing audio narration…",
        title,
        f"{meta}\n\n{story_body}",
        img_path,
        None,
        history,
    )

    # 4. Generate audio
    try:
        audio_path = audio_engine.narrate(title, story_body)
    except Exception:
        audio_path = None

    yield (
        " Story complete!",
        title,
        f"{meta}\n\n{story_body}",
        img_path,
        audio_path,
        history,
    )


# ── Continue story ────────────────────────────────────────────────────────────
def continue_story(current_story_text, region, theme, mood, history):
    if not current_story_text or len(current_story_text.strip()) < 50:
        yield (" Generate a story first before continuing.", "", current_story_text, None, None, history)
        return

    yield (" Continuing the story…", "", current_story_text, None, None, history)

    try:
        title, continuation, image_prompt = story_engine.continue_story(
            existing=current_story_text,
            region=region,
            theme=theme,
            mood=mood,
        )
        full_text = current_story_text + "\n\n— ✦ —\n\n" + continuation
        history = session_mgr.add_story(history, title + " (continued)", full_text, region, theme, mood)

        img_path = image_engine.generate(image_prompt)
        audio_path = audio_engine.narrate(title, continuation)

        yield ("Story continued!", title, full_text, img_path, audio_path, history)
    except Exception as e:
        yield (f" Error: {e}", "", current_story_text, None, None, history)


# ── Download story as .txt ────────────────────────────────────────────────────
def download_story(title, story_text):
    if not story_text:
        return None
    path = f"/tmp/{title.replace(' ', '_')[:40]}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n{'='*len(title)}\n\n{story_text}\n\n— Generated by Smart Cultural Storyteller")
    return path


# ── Build Gradio UI ───────────────────────────────────────────────────────────
def build_ui():
    with gr.Blocks(
        
        title="Smart Cultural Storyteller",
        theme=gr.themes.Base(
            font=[gr.themes.GoogleFont("Crimson Pro"), "Georgia", "serif"],
        ),
    ) as demo:

        # State
        history_state = gr.State([])
        story_title_state = gr.State("")

        # ── Banner ──
        gr.HTML("""
        <div id="banner">
            <h1> Smart Cultural Storyteller</h1>
            <p>Preserving the oral traditions of Rural India through AI — every story has a soul</p>
        </div>
        """)

        with gr.Tabs():

            # ════════════════════════════════════════
            # TAB 1 — GENERATE
            # ════════════════════════════════════════
            with gr.Tab(" Generate Story"):
                with gr.Row():

                    # LEFT — Controls
                    with gr.Column(scale=4):
                        gr.HTML('<p class="section-header">Craft Your Story</p>')

                        region = gr.Dropdown(
                            choices=REGIONS, value=REGIONS[0],
                            label="Region", interactive=True
                        )
                        theme = gr.Dropdown(
                            choices=THEMES, value=THEMES[0],
                            label="Theme", interactive=True
                        )
                        with gr.Row():
                            mood = gr.Dropdown(
                                choices=MOODS, value=MOODS[0],
                                label="Mood", interactive=True
                            )
                            length_label = gr.Dropdown(
                                choices=list(LENGTHS.keys()),
                                value=list(LENGTHS.keys())[1],
                                label="Length", interactive=True
                            )
                        extra_details = gr.Textbox(
                            label="Characters / Extra Details (optional)",
                            placeholder="e.g. An old weaver named Ramu and his granddaughter Priya on a monsoon evening…",
                            lines=3, max_lines=5,
                        )

                        with gr.Row():
                            gen_btn = gr.Button(" Tell Me a Story", variant="primary", scale=3)
                            cont_btn = gr.Button(" Continue", variant="secondary", scale=1)

                        status_box = gr.Textbox(
                            label="", elem_id="status-box",
                            interactive=False, show_label=False,
                            placeholder="Status will appear here…"
                        )

                    # RIGHT — Output
                    with gr.Column(scale=6):
                        story_title_box = gr.Textbox(
                            label="Title", elem_id="story-title-box",
                            interactive=False, show_label=False,
                        )
                        story_output_box = gr.Textbox(
                            label="Story", elem_id="story-output-box",
                            interactive=False, show_label=False,
                            lines=14, max_lines=30,
                        )

                        with gr.Row():
                            story_image = gr.Image(
                                label="Illustration", elem_id="story-image",
                                type="filepath", interactive=False,
                                height=280,
                            )

                        audio_player = gr.Audio(
                            label="🎵 Listen to the Story", elem_id="audio-player",
                            type="filepath", interactive=False,
                        )

                        with gr.Row():
                            dl_btn = gr.Button("↓ Save as TXT", variant="secondary")
                            dl_file = gr.File(label="Download", visible=True)

            # ════════════════════════════════════════
            # TAB 2 — HISTORY
            # ════════════════════════════════════════
            with gr.Tab(" My Stories"):
                gr.HTML('<p class="section-header">Stories You Have Generated This Session</p>')
                history_display = gr.Dataframe(
                    headers=["Title", "Region", "Theme", "Mood", "Generated At"],
                    datatype=["str", "str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                )
                refresh_btn = gr.Button("↺ Refresh History", variant="secondary")

            # ════════════════════════════════════════
            # TAB 3 — DISCOVER
            # ════════════════════════════════════════
            with gr.Tab(" Discover"):
                gr.HTML('<p class="section-header">Curated Cultural Stories</p>')
                gr.Markdown("""
These hand-curated stories from `data/stories.json` showcase authentic Rural Indian folk narratives.
Click any story to read it in the Generate tab.
                """)
                discover_display = gr.Dataframe(
                    headers=["Title", "Region", "Theme", "Mood", "Excerpt"],
                    datatype=["str","str","str","str","str"],
                    interactive=False, wrap=True,
                )
                load_discover_btn = gr.Button("Load Stories", variant="secondary")

            # ════════════════════════════════════════
            # TAB 4 — SETTINGS
            # ════════════════════════════════════════
            with gr.Tab(" Settings"):
                gr.HTML('<p class="section-header">AI & Application Settings</p>')
                gr.Markdown("""
Configure your AI provider and voice settings. All keys are stored **locally only** in your `.env` file.
                """)
                with gr.Accordion("AI Model", open=True):
                    ai_provider = gr.Dropdown(
                        choices=["groq", "openai", "anthropic"],
                        value=os.getenv("AI_PROVIDER", "groq"),
                        label="Provider",
                    )
                    gr.Markdown("**Groq** is free and fast — recommended. Get a key at [console.groq.com](https://console.groq.com)")

                with gr.Accordion("Audio Settings", open=False):
                    tts_speed = gr.Slider(0.5, 2.0, value=0.9, step=0.1, label="Narration Speed")
                    tts_lang  = gr.Dropdown(["en", "hi"], value="en", label="Narration Language")

                with gr.Accordion("Image Settings", open=False):
                    img_style = gr.Dropdown(
                        ["Watercolour folk art", "Madhubani painting style", "Warli tribal art",
                         "Realistic photography", "Oil painting"],
                        value="Watercolour folk art",
                        label="Illustration Style",
                    )

                save_settings_btn = gr.Button("Save Settings", variant="primary")
                settings_msg = gr.Textbox(label="", interactive=False, show_label=False)

        # ── Footer ──
        gr.HTML("""
        <div style="text-align:center;padding:1.5rem;font-family:'Crimson Pro',serif;
                    font-style:italic;font-size:0.9rem;color:#7a6245;
                    border-top:1px solid rgba(180,130,50,0.2);margin-top:1rem;">
            © 2026 Smart Cultural Storyteller · Made with ❤️ to preserve the stories of Rural India
        </div>
        """)

        # ── Event wiring ─────────────────────────────────────────────────────
        gen_btn.click(
            fn=generate_story,
            inputs=[region, theme, mood, length_label, extra_details, history_state],
            outputs=[status_box, story_title_box, story_output_box,
                     story_image, audio_player, history_state],
        )

        cont_btn.click(
            fn=continue_story,
            inputs=[story_output_box, region, theme, mood, history_state],
            outputs=[status_box, story_title_box, story_output_box,
                     story_image, audio_player, history_state],
        )

        dl_btn.click(
            fn=download_story,
            inputs=[story_title_box, story_output_box],
            outputs=[dl_file],
        )

        def refresh_history(history):
            if not history:
                return []
            rows = [[s["title"], s["region"], s["theme"], s["mood"], s["created_at"]]
                    for s in history]
            return rows

        refresh_btn.click(fn=refresh_history, inputs=[history_state], outputs=[history_display])

        def load_discover():
            from data.loader import load_stories
            stories = load_stories()
            rows = [[s.get("title",""), s.get("region",""), s.get("theme",""),
                     s.get("mood",""), s.get("excerpt","")[:80]+"…"] for s in stories]
            return rows

        load_discover_btn.click(fn=load_discover, outputs=[discover_display])

        def save_settings(provider, speed, lang, style):
            story_engine.set_provider(provider)
            audio_engine.set_speed(speed)
            audio_engine.set_language(lang)
            image_engine.set_style(style)
            return "✅ Settings saved."

        save_settings_btn.click(
            fn=save_settings,
            inputs=[ai_provider, tts_speed, tts_lang, img_style],
            outputs=[settings_msg],
        )

    return demo


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        
        
    )
