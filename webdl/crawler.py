from __future__ import annotations

from urllib.parse import urlparse

import requests

from .extractor import extract_links
from .models import AnalysisReport


def _merge_unique(target: list[str], values: list[str]) -> None:
    known = set(target)
    for value in values:
        if value not in known:
            target.append(value)
            known.add(value)


def _should_scan(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return host.endswith("websiteedukasi.com")


def _derive_scope_keyword(start_url: str) -> str | None:
    path = urlparse(start_url).path.lower()
    if "kelas-" not in path:
        return None
    idx = path.find("kelas-")
    if idx < 0:
        return None
    snippet = path[idx : idx + 9]
    if snippet.startswith("kelas-"):
        return snippet
    return None


def fetch_html(session: requests.Session, url: str, timeout: int = 30) -> str:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def analyze_site(start_url: str, max_pages: int = 30) -> AnalysisReport:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; webdl/1.0)"})

    report = AnalysisReport(start_url=start_url)
    queue = [start_url]
    seen: set[str] = set()
    scope_keyword = _derive_scope_keyword(start_url)

    while queue and len(report.pages_scanned) < max_pages:
        current = queue.pop(0)
        if current in seen:
            continue
        seen.add(current)

        if not _should_scan(current):
            continue

        html_text = fetch_html(session, current)
        report.pages_scanned.append(current)

        links = extract_links(html_text, current)
        _merge_unique(report.modul_pages, links.modul_pages)
        _merge_unique(report.download_pages, links.download_pages)
        _merge_unique(report.direct_files, links.direct_files)

        new_download_pages: list[str] = []
        new_modul_pages: list[str] = []

        for url in links.download_pages:
            if url in seen or url in queue:
                continue
            new_download_pages.append(url)

        for url in links.modul_pages:
            if url in seen or url in queue:
                continue
            if scope_keyword and scope_keyword not in url.lower():
                continue
            new_modul_pages.append(url)

        for url in reversed(new_download_pages):
            queue.insert(0, url)
        for url in new_modul_pages:
            queue.append(url)

    return report
