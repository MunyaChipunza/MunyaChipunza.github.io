from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def main() -> int:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        print("Set ELEVENLABS_API_KEY first, then run this again.", file=sys.stderr)
        return 1

    request = Request(
        "https://api.elevenlabs.io/v1/voices",
        headers={"Accept": "application/json", "xi-api-key": api_key},
        method="GET",
    )
    try:
        with urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        print(f"ElevenLabs returned HTTP {error.code}: {details[:600]}", file=sys.stderr)
        return 1

    voices = data.get("voices", [])
    if not voices:
        print("No voices found on this ElevenLabs account.")
        return 0

    for voice in voices:
        print(f"{voice.get('name', '(unnamed)')}  |  {voice.get('voice_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
