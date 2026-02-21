from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import requests


def _extract_drive_confirm_request(html_text: str) -> tuple[str, dict[str, str]] | None:
    if "download-form" not in html_text:
        return None

    action_match = re.search(r'<form[^>]+id="download-form"[^>]+action="([^"]+)"', html_text)
    if not action_match:
        return None

    params: dict[str, str] = {}
    for name, value in re.findall(r'<input[^>]+name="([^"]+)"[^>]+value="([^"]*)"', html_text):
        params[name] = value

    if "id" not in params:
        return None

    return unquote(action_match.group(1)), params


def guess_filename(url: str, headers: dict[str, str]) -> str:
    content_disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', content_disposition)
    if match:
        return unquote(match.group(1).strip())

    parsed = urlparse(url)
    query_id = parse_qs(parsed.query).get("id")
    if query_id:
        return query_id[0]

    name = Path(parsed.path).name
    if name:
        return unquote(name)

    return "download.bin"


def download_file(session: requests.Session, url: str, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)

    response = session.get(url, stream=True, timeout=60)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "").lower()
    parsed = urlparse(response.url)
    is_drive = "drive.google.com" in parsed.netloc or "drive.usercontent.google.com" in parsed.netloc

    if is_drive and "text/html" in content_type:
        html_text = response.text
        confirm_request = _extract_drive_confirm_request(html_text)
        if confirm_request:
            action_url, params = confirm_request
            response = session.get(action_url, params=params, stream=True, timeout=60)
            response.raise_for_status()

    filename = guess_filename(response.url, dict(response.headers))
    target = destination_dir / filename

    with target.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            if chunk:
                handle.write(chunk)

    return target
