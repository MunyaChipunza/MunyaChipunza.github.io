from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DRAFT_PATH = ROOT / "new-post.txt"
TEMPLATE_PATH = ROOT / "NEW-POST-TEMPLATE.txt"
CONTENT_POSTS_DIR = ROOT / "content" / "posts"
SUBMITTED_DIR = ROOT / "content" / "submitted"
GOOGLE_DRIVE_TARGET = Path(r"G:\My Drive\100. Zee\Munyachipunza.com")
SITE_URL = "https://munyachipunza.com"
REPO = "MunyaChipunza/MunyaChipunza.github.io"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a new MunyaChipunza.com reflection.")
    parser.add_argument(
        "--draft",
        default=str(DEFAULT_DRAFT_PATH),
        help="Path to the draft text file. Defaults to new-post.txt in this repository.",
    )
    return parser.parse_args(argv)


def run(command: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"> {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
    )
    if capture:
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def split_metadata_and_body(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()

    metadata: dict[str, str] = {}
    body_start = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            body_start = index + 1
            break
        if stripped == "---":
            body_start = index + 1
            break
        match = re.match(r"^(title|tag|summary|date)\s*:\s*(.+)$", stripped, flags=re.IGNORECASE)
        if match:
            metadata[match.group(1).lower()] = match.group(2).strip()
            body_start = index + 1
            continue
        if "title" not in metadata:
            metadata["title"] = stripped.lstrip("#").strip()
            body_start = index + 1
            break

    body_lines = lines[body_start:]
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    return metadata, body_lines


def paragraphs_from_lines(lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == "---":
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current).strip())
    return paragraphs


def text_snippet(text: str, limit: int) -> str:
    text = " ".join(text.split()).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].strip() + "."


def reading_minutes(paragraphs: list[str]) -> int:
    words = re.findall(r"\b\w+\b", " ".join(paragraphs))
    return max(2, math.ceil(len(words) / 230))


def post_date_iso(metadata: dict[str, str]) -> tuple[str, str]:
    date_value = metadata.get("date")
    if date_value:
        parsed = datetime.strptime(date_value, "%Y-%m-%d")
    else:
        parsed = datetime.now()
    # Noon UTC keeps the displayed date aligned with the South Africa calendar day.
    iso_value = f"{parsed:%Y-%m-%d}T12:00:00Z"
    file_prefix = f"{parsed:%Y-%m-%d}"
    return iso_value, file_prefix


def parse_draft(draft_path: Path) -> tuple[dict, Path]:
    text = draft_path.read_text(encoding="utf-8")
    metadata, body_lines = split_metadata_and_body(text)
    title = metadata.get("title", "").strip()
    paragraphs = paragraphs_from_lines(body_lines)

    if not title or title.lower() == "paste your title here":
        raise RuntimeError(f"{draft_path} needs a real TITLE line before publishing.")
    if not paragraphs or paragraphs[0].lower() == "paste the body here.":
        raise RuntimeError(f"{draft_path} needs the post body before publishing.")

    route = slugify(title)
    if not route:
        raise RuntimeError("Could not create a URL slug from the title.")

    published_date, file_prefix = post_date_iso(metadata)
    summary = metadata.get("summary") or text_snippet(paragraphs[0], 180)
    post = {
        "old_slug": route,
        "route": route,
        "tag": metadata.get("tag", "Reflection"),
        "title": title,
        "summary": summary,
        "excerpt": summary,
        "published_date": published_date,
        "updated_date": published_date,
        "minutes_to_read": reading_minutes(paragraphs),
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
        "paragraphs": paragraphs,
    }
    post_path = CONTENT_POSTS_DIR / f"{file_prefix}-{route}.json"
    return post, post_path


def assert_clean_worktree() -> None:
    result = run(["git", "status", "--porcelain"], capture=True)
    if result.stdout.strip():
        raise RuntimeError("Git working tree is not clean. Commit or stash existing changes before publishing.")


def sync_main_branch() -> None:
    run(["git", "switch", "main"])
    run(["git", "pull", "--ff-only", "origin", "main"])


def write_post_file(post: dict, post_path: Path) -> None:
    if post_path.exists():
        raise RuntimeError(f"Post file already exists: {post_path}")
    CONTENT_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    post_path.write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_generated_site(post: dict) -> None:
    page_path = ROOT / "writing" / post["route"] / "index.html"
    if not page_path.exists():
        raise RuntimeError(f"Generated page is missing: {page_path}")
    page = page_path.read_text(encoding="utf-8")
    required = [post["title"], post["paragraphs"][0]]
    for value in required:
        escaped = html.escape(value, quote=False).replace("&#x27;", "'")
        if value not in page and escaped not in page:
            raise RuntimeError(f"Generated page does not contain expected text: {value[:80]}")

    bad_patterns = ["&#x27;", "&amp;#", "â€™", "â€œ", "â€�"]
    for html_path in ROOT.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8", errors="replace")
        for pattern in bad_patterns:
            if pattern in text:
                raise RuntimeError(f"Encoding artifact {pattern!r} found in {html_path}")


def wait_for_run(run_id: str, label: str, timeout_seconds: int = 420) -> str:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        result = run(
            ["gh", "run", "view", run_id, "--repo", REPO, "--json", "status,conclusion"],
            capture=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            status = data.get("status")
            conclusion = data.get("conclusion")
            print(f"{label}: {status} {conclusion or ''}".strip())
            if status == "completed":
                return conclusion or ""
        time.sleep(10)
    raise RuntimeError(f"Timed out waiting for {label}.")


def latest_run_id(*, workflow: str | None = None, commit: str | None = None, event: str | None = None) -> str | None:
    command = ["gh", "run", "list", "--repo", REPO, "--limit", "20", "--json", "databaseId,workflowName,headSha,event,createdAt"]
    if workflow:
        command.extend(["--workflow", workflow])
    result = run(command, capture=True, check=False)
    if result.returncode != 0:
        return None
    for item in json.loads(result.stdout or "[]"):
        if commit and item.get("headSha") != commit:
            continue
        if event and item.get("event") != event:
            continue
        return str(item["databaseId"])
    return None


def wait_for_deploy_and_notification(commit: str) -> None:
    if not command_exists("gh"):
        print("gh CLI not found; skipping deployment and notification confirmation.")
        return

    print("Waiting for GitHub Pages deployment...")
    pages_run = None
    for _ in range(24):
        pages_run = latest_run_id(commit=commit, workflow="pages-build-deployment")
        if pages_run:
            break
        time.sleep(5)
    if pages_run:
        pages_result = wait_for_run(pages_run, "GitHub Pages")
        if pages_result != "success":
            raise RuntimeError(f"GitHub Pages finished with {pages_result}.")
    else:
        print("Could not find the GitHub Pages run; continuing to live URL verification.")

    print("Waiting for Buttondown notification...")
    notify_run = None
    for _ in range(24):
        notify_run = latest_run_id(commit=commit, workflow="Notify subscribers")
        if notify_run:
            break
        time.sleep(5)

    if not notify_run:
        print("Could not find notification run; continuing without notification confirmation.")
        return

    notify_result = wait_for_run(notify_run, "Notify subscribers")
    if notify_result == "success":
        return

    print("Notification failed once. Rerunning it once in case Buttondown timed out.")
    run(["gh", "workflow", "run", "notify-subscribers.yml", "--repo", REPO, "-f", "status=about_to_send"])
    time.sleep(8)
    rerun_id = latest_run_id(workflow="Notify subscribers", event="workflow_dispatch")
    if not rerun_id:
        raise RuntimeError("Could not find rerun notification workflow.")
    rerun_result = wait_for_run(rerun_id, "Notify subscribers rerun")
    if rerun_result != "success":
        raise RuntimeError(f"Notification rerun finished with {rerun_result}.")


def verify_live_page(post: dict) -> None:
    url = f"{SITE_URL}/writing/{post['route']}/"
    print(f"Checking live page: {url}")
    deadline = time.time() + 300
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=30) as response:
                body = response.read().decode("utf-8", errors="replace")
            title = html.escape(post["title"], quote=False).replace("&#x27;", "'")
            final_paragraph = html.escape(post["paragraphs"][-1], quote=False).replace("&#x27;", "'")
            if response.status == 200 and title in body and final_paragraph in body:
                print(f"Live: {url}")
                return
        except Exception as error:
            print(f"Live check not ready yet: {error}")
        time.sleep(10)
    raise RuntimeError(f"Live page did not verify within 5 minutes: {url}")


def mirror_to_google_drive() -> None:
    if not GOOGLE_DRIVE_TARGET.exists():
        print(f"Google Drive target not found; skipping mirror: {GOOGLE_DRIVE_TARGET}")
        return
    if not (ROOT / "index.html").exists():
        raise RuntimeError(f"Source does not look like the site root: {ROOT}")

    command = [
        "robocopy",
        str(ROOT),
        str(GOOGLE_DRIVE_TARGET),
        "/MIR",
        "/XJ",
        "/XD",
        ".git",
        "/R:2",
        "/W:2",
        "/NFL",
        "/NDL",
        "/NP",
    ]
    result = run(command, check=False)
    if result.returncode > 7:
        raise RuntimeError(f"Robocopy failed with exit code {result.returncode}.")
    print(f"Google Drive mirror updated: {GOOGLE_DRIVE_TARGET}")


def reset_draft(post: dict, draft_path: Path) -> None:
    SUBMITTED_DIR.mkdir(parents=True, exist_ok=True)
    submitted_path = SUBMITTED_DIR / f"{post['published_date'][:10]}-{post['route']}.txt"
    shutil.copy2(draft_path, submitted_path)
    shutil.copy2(TEMPLATE_PATH, draft_path)
    print(f"Archived submitted draft: {submitted_path}")
    print(f"Reset draft for the next post: {draft_path}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    draft_path = Path(args.draft).expanduser().resolve()

    if not draft_path.exists():
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TEMPLATE_PATH, draft_path)
        print(f"Created draft file: {draft_path}")
        print("Paste your post into it, save, then run publish-post.bat again.")
        return 1

    post, post_path = parse_draft(draft_path)
    print(f"Preparing: {post['title']}")
    print(f"URL: {SITE_URL}/writing/{post['route']}/")

    assert_clean_worktree()
    sync_main_branch()
    assert_clean_worktree()
    write_post_file(post, post_path)
    run([sys.executable, "scripts/generate_audio.py", "--route", post["route"], "--skip-if-unconfigured"])
    run([sys.executable, "scripts/generate_writing.py"])
    validate_generated_site(post)
    run(["git", "add", "--all"])
    run(["git", "commit", "-m", f"Add {post['title']} reflection"])
    commit = run(["git", "rev-parse", "HEAD"], capture=True).stdout.strip()
    run(["git", "push", "origin", "main"])
    wait_for_deploy_and_notification(commit)
    verify_live_page(post)
    reset_draft(post, draft_path)
    mirror_to_google_drive()
    print(f"Done: {SITE_URL}/writing/{post['route']}/")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
