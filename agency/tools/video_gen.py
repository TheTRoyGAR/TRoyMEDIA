"""
Real Google Veo 3.1 video generation via the Gemini API.

Deliberately NOT wired into any CrewAI agent's tool list. Video generation
costs real money per second ($0.05-$0.40/sec depending on model tier), and an
agent with autonomous access to this tool during a normal planning run could
trigger real charges without a human approving each clip. This module is
called directly, one clip at a time, only when a human has decided to
actually produce that specific clip.

Requires GEMINI_API_KEY in .env (same key used for Gemini access generally,
separate from ANTHROPIC_API_KEY). Get one at https://aistudio.google.com/apikey
"""

import os
import time
from pathlib import Path

from google import genai
from google.genai import types


VEO_MODEL = "veo-3.1-generate-preview"
VEO_MODEL_FAST = "veo-3.1-fast-generate-preview"

# Real per-second pricing via the Gemini API (confirmed 2026-08-24):
# Lite 720p: $0.05/sec, Fast 720p: $0.10/sec, Standard 720p/1080p: $0.40/sec.
# This module uses the Standard model by default (best quality); pass
# fast=True for the cheaper/faster tier.


def generate_veo_clip(
    prompt: str,
    duration_seconds: int = 8,
    output_path: str | None = None,
    fast: bool = False,
    poll_interval_seconds: int = 20,
) -> str:
    """
    Generate one real video clip via Veo 3.1. Blocks until the clip is ready
    (video generation is asynchronous on Google's side, typically a few
    minutes). Returns the path to the downloaded video file.

    Costs real money — see module docstring. Call this once per clip you've
    actually decided to produce, never in a loop without reviewing cost.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set in .env. Get one at https://aistudio.google.com/apikey"
        )

    client = genai.Client(api_key=api_key)
    model = VEO_MODEL_FAST if fast else VEO_MODEL

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            duration_seconds=duration_seconds,
        ),
    )

    while not operation.done:
        time.sleep(poll_interval_seconds)
        operation = client.operations.get(operation)

    video = operation.response.generated_videos[0].video

    if output_path is None:
        safe_name = "".join(c if c.isalnum() else "_" for c in prompt[:40])
        output_path = str(Path(__file__).resolve().parents[2] / "video_output" / f"{safe_name}.mp4")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    video.save(output_path)
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_gen.py \"<prompt>\" [duration_seconds] [--fast]")
        sys.exit(1)

    prompt_arg = sys.argv[1]
    duration_arg = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8
    fast_arg = "--fast" in sys.argv

    print(f"Generating clip (model={'fast' if fast_arg else 'standard'}, {duration_arg}s)...")
    path = generate_veo_clip(prompt_arg, duration_seconds=duration_arg, fast=fast_arg)
    print(f"Saved to: {path}")
