from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEDULED_DIR = ROOT / "content" / "scheduled"
POSTS_DIR = ROOT / "content" / "posts"


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print(f"> {' '.join(command)}")
    result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace")
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def parse_iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def scheduled_files() -> list[Path]:
    if not SCHEDULED_DIR.exists():
        return []
    return sorted(path for path in SCHEDULED_DIR.glob("*.json") if path.is_file())


def publish_due_posts(now: datetime) -> list[dict]:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    published: list[dict] = []

    for path in scheduled_files():
        post = json.loads(path.read_text(encoding="utf-8"))
        scheduled_at = parse_iso(post["scheduled_publish_at"])
        if scheduled_at > now:
            print(f"Not due yet: {post['title']} at {scheduled_at.isoformat()}")
            continue

        post.pop("scheduled_publish_at", None)
        post.pop("scheduled_local_time", None)
        post.pop("timezone", None)
        post.pop("draft", None)

        target = POSTS_DIR / f"{post['published_date'][:10]}-{post['route']}.json"
        if target.exists():
            raise RuntimeError(f"Refusing to overwrite existing post: {target}")

        target.write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        archive = SCHEDULED_DIR / "published"
        archive.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), archive / path.name)
        published.append(post)
        print(f"Scheduled post moved into posts: {target}")

    return published


def generate_audio(post: dict) -> None:
    result = run(
        [sys.executable, "scripts/generate_audio.py", "--route", post["route"], "--skip-if-unconfigured"],
        check=False,
    )
    if result.returncode != 0:
        print(f"Audio generation did not complete for {post['route']}; continuing without audio.")


def commit_and_push(posts: list[dict]) -> None:
    run(["git", "config", "user.name", "github-actions[bot]"])
    run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    run(["git", "add", "--all"])
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if not status.stdout.strip():
        print("No generated changes to commit.")
        return

    if len(posts) == 1:
        message = f"Publish scheduled reflection: {posts[0]['title']}"
    else:
        message = f"Publish {len(posts)} scheduled reflections"
    run(["git", "commit", "-m", message])
    run(["git", "push"])


def notify_subscribers() -> None:
    if not os.getenv("BUTTONDOWN_API_KEY"):
        print("BUTTONDOWN_API_KEY is not configured; skipping subscriber notification.")
        return
    os.environ.setdefault("BUTTONDOWN_EMAIL_STATUS", "about_to_send")
    run([sys.executable, "scripts/notify_buttondown.py"])


def main() -> int:
    now_value = os.getenv("SCHEDULED_PUBLISH_NOW")
    now = parse_iso(now_value) if now_value else datetime.now(timezone.utc)
    print(f"Checking scheduled posts at {now.isoformat()}")

    published = publish_due_posts(now)
    if not published:
        print("No scheduled posts are due.")
        return 0

    for post in published:
        generate_audio(post)

    run([sys.executable, "scripts/generate_writing.py"])
    if os.getenv("SCHEDULED_PUBLISH_DRY_RUN") == "1":
        print("Dry run complete; skipping commit and push.")
        return 0

    commit_and_push(published)
    notify_subscribers()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
