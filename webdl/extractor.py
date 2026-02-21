from __future__ import annotations

import html
import re
from urllib.parse import urljoin, urlparse

from .models import ExtractedLinks

FILE_EXTENSIONS = (
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".zip",
    ".rar",
    ".7z",
)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _collect_attr_urls(html_text: str, base_url: str) -> list[str]:
    pattern = re.compile(r"(?:href|src|action)=[\"']([^\"']+)[\"']", re.IGNORECASE)
    urls: list[str] = []
    for raw in pattern.findall(html_text):
        clean = html.unescape(raw.strip())
        if not clean:
            continue
        if clean.startswith("javascript:") or clean.startswith("#"):
            continue
        urls.append(urljoin(base_url, clean))
    return urls


def _is_direct_file(url: str) -> bool:
    parsed = urlparse(url)
    lowered = parsed.path.lower()
    if lowered.endswith(FILE_EXTENSIONS):
        return True
    if "drive.google.com" in parsed.netloc and "export=download" in parsed.query:
        return True
    return False


def extract_links(html_text: str, base_url: str) -> ExtractedLinks:
    urls = _collect_attr_urls(html_text, base_url)

    modul_pages: list[str] = []
    download_pages: list[str] = []
    direct_files: list[str] = []

    for url in urls:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.lower()

        if _is_direct_file(url):
            direct_files.append(url)
            continue

        if host.endswith("websiteedukasi.com"):
            if path.startswith("/modul-ajar") and path.endswith(".html"):
                modul_pages.append(url)
            if path.startswith("/download/") and len(path) > len("/download/"):
                download_pages.append(url)

    return ExtractedLinks(
        modul_pages=_dedupe(modul_pages),
        download_pages=_dedupe(download_pages),
        direct_files=_dedupe(direct_files),
    )
