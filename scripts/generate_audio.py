from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "assets" / "audio"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
CHUNK_LIMIT = 4300
MAX_RETRIES = 4
RETRY_HTTP_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
_WRITING_GENERATOR = None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate post audio files with ElevenLabs.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--route", help="Generate audio for one post route.")
    target.add_argument("--missing", action="store_true", help="Generate audio for posts that do not have MP3 files yet.")
    target.add_argument("--all", action="store_true", help="Generate audio for every post.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing audio files.")
    parser.add_argument(
        "--skip-if-unconfigured",
        action="store_true",
        help="Exit cleanly if ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID is missing.",
    )
    return parser.parse_args(argv)


def load_writing_generator():
    global _WRITING_GENERATOR
    if _WRITING_GENERATOR is not None:
        return _WRITING_GENERATOR
    module_path = ROOT / "scripts" / "generate_writing.py"
    spec = importlib.util.spec_from_file_location("generate_writing", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _WRITING_GENERATOR = module
    return module


def load_posts() -> list[dict]:
    generator = load_writing_generator()
    posts = generator.load_content_posts() + [dict(post) for post in generator.LOCAL_POSTS]
    posts.sort(key=lambda post: post["published_date"], reverse=True)
    return posts


def html_to_plain(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"</p\s*>", "\n\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def post_audio_text(post: dict) -> str:
    generator = load_writing_generator()
    paragraphs = [html_to_plain(paragraph) for paragraph in generator.paragraph_text(post)]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    return "\n\n".join([post["title"], *paragraphs]).strip()


def split_long_piece(piece: str, limit: int) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", piece)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not sentence:
            continue
        if len(sentence) > limit:
            if current:
                chunks.append(current.strip())
                current = ""
            for index in range(0, len(sentence), limit):
                chunks.append(sentence[index : index + limit].strip())
            continue
        if current and len(current) + len(sentence) + 1 > limit:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current.strip())
    return chunks


def split_for_elevenlabs(text: str, limit: int = CHUNK_LIMIT) -> list[str]:
    pieces = [piece.strip() for piece in text.split("\n\n") if piece.strip()]
    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if len(piece) > limit:
            if current:
                chunks.append(current.strip())
                current = ""
            chunks.extend(split_long_piece(piece, limit))
            continue
        candidate = f"{current}\n\n{piece}".strip() if current else piece
        if len(candidate) > limit:
            chunks.append(current.strip())
            current = piece
        else:
            current = candidate
    if current:
        chunks.append(current.strip())
    return chunks


def float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw in (None, ""):
        return default
    return float(raw)


def bool_env(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw in (None, ""):
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def elevenlabs_request(text: str, *, api_key: str, voice_id: str) -> bytes:
    model_id = os.environ.get("ELEVENLABS_MODEL_ID", DEFAULT_MODEL_ID)
    output_format = os.environ.get("ELEVENLABS_OUTPUT_FORMAT", DEFAULT_OUTPUT_FORMAT)
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": float_env("ELEVENLABS_STABILITY", 0.45),
            "similarity_boost": float_env("ELEVENLABS_SIMILARITY_BOOST", 0.8),
            "style": float_env("ELEVENLABS_STYLE", 0.0),
            "use_speaker_boost": bool_env("ELEVENLABS_USE_SPEAKER_BOOST", True),
        },
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{quote(voice_id)}?output_format={quote(output_format)}"
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        },
        method="POST",
    )
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(request, timeout=180) as response:
                return response.read()
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            if error.code not in RETRY_HTTP_CODES or attempt == MAX_RETRIES:
                raise RuntimeError(f"ElevenLabs returned HTTP {error.code}: {details[:600]}") from error
            print(f"ElevenLabs HTTP {error.code}; retrying request {attempt + 1}/{MAX_RETRIES}")
        except (ConnectionResetError, TimeoutError, URLError, OSError) as error:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"ElevenLabs request failed after {MAX_RETRIES} attempts: {error}") from error
            print(f"ElevenLabs connection issue; retrying request {attempt + 1}/{MAX_RETRIES}")
        time.sleep(min(2 * attempt, 10))
    raise RuntimeError("ElevenLabs request failed unexpectedly.")


def selected_posts(posts: list[dict], args: argparse.Namespace) -> list[dict]:
    if args.route:
        matches = [post for post in posts if post["route"] == args.route]
        if not matches:
            raise RuntimeError(f"No post found with route: {args.route}")
        return matches
    if args.all:
        return posts
    return [post for post in posts if not (AUDIO_DIR / f"{post['route']}.mp3").exists()]


def assert_configured(skip_if_unconfigured: bool) -> tuple[str, str] | None:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
    if api_key and voice_id:
        return api_key, voice_id
    message = "ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID must be set before audio can be generated."
    if skip_if_unconfigured:
        print(f"Skipping audio: {message}")
        return None
    raise RuntimeError(message)


def generate_post_audio(post: dict, *, api_key: str, voice_id: str, force: bool) -> Path:
    output_path = AUDIO_DIR / f"{post['route']}.mp3"
    if output_path.exists() and not force:
        print(f"Exists: {output_path}")
        return output_path

    text = post_audio_text(post)
    chunks = split_for_elevenlabs(text)
    if not chunks:
        raise RuntimeError(f"No readable text found for {post['route']}")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating {output_path.name} ({len(chunks)} request{'s' if len(chunks) != 1 else ''})")
    audio_parts = [elevenlabs_request(chunk, api_key=api_key, voice_id=voice_id) for chunk in chunks]

    with tempfile.NamedTemporaryFile("wb", delete=False, dir=AUDIO_DIR, suffix=".tmp") as temp_file:
        temp_path = Path(temp_file.name)
        for part in audio_parts:
            temp_file.write(part)
    temp_path.replace(output_path)
    return output_path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = assert_configured(args.skip_if_unconfigured)
    if config is None:
        return 0
    api_key, voice_id = config

    posts = selected_posts(load_posts(), args)
    if not posts:
        print("No audio files needed.")
        return 0

    for post in posts:
        generate_post_audio(post, api_key=api_key, voice_id=voice_id, force=args.force)
    print(f"Audio complete: {len(posts)} post(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
