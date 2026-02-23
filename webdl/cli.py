from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import requests

from .crawler import analyze_site
from .downloader import download_file


def _parse_grade_spec(spec: str) -> list[int]:
    values: list[int] = []
    for part in spec.split(","):
        piece = part.strip()
        if not piece:
            continue
        if "-" in piece:
            start_text, end_text = piece.split("-", maxsplit=1)
            start = int(start_text)
            end = int(end_text)
            if start > end:
                start, end = end, start
            for grade in range(start, end + 1):
                if grade not in values:
                    values.append(grade)
            continue
        grade = int(piece)
        if grade not in values:
            values.append(grade)
    return values


def _build_class_urls(classes_spec: str, exclude_spec: str = "") -> list[str]:
    classes = _parse_grade_spec(classes_spec)
    excluded = set(_parse_grade_spec(exclude_spec)) if exclude_spec.strip() else set()
    selected = [grade for grade in classes if grade not in excluded]
    return [f"https://www.websiteedukasi.com/modul-ajar-kelas-{grade}.html" for grade in selected]


def _download_from_url(url: str, max_pages: int, limit: int | None, out_dir: Path) -> int:
    report = analyze_site(url, max_pages=max_pages)
    if not report.direct_files:
        print(f"No direct file links found: {url}")
        return 1

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; webdl/1.0)"})

    selected = report.direct_files[:limit] if limit is not None else report.direct_files
    for link in selected:
        try:
            output_path = download_file(session, link, out_dir)
            print(f"Downloaded: {output_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"Failed: {link} ({exc})")
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    report = analyze_site(args.url, max_pages=args.max_pages)

    print(f"Scanned pages: {len(report.pages_scanned)}")
    print(f"Modul pages: {len(report.modul_pages)}")
    print(f"Download pages: {len(report.download_pages)}")
    print(f"Direct files: {len(report.direct_files)}")

    for link in report.direct_files:
        print(link)

    if args.output:
        Path(args.output).write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        print(f"Saved analysis to {args.output}")

    return 0


def cmd_download(args: argparse.Namespace) -> int:
    return _download_from_url(args.url, args.max_pages, args.limit, Path(args.out))


def cmd_download_classes(args: argparse.Namespace) -> int:
    urls = _build_class_urls(args.classes, args.exclude)
    if not urls:
        print("No class URLs selected.")
        return 1

    status = 0
    for url in urls:
        grade = url.rsplit("kelas-", maxsplit=1)[-1].split(".html", maxsplit=1)[0]
        out_dir = Path(args.out) / f"kelas-{grade}"
        print(f"[kelas-{grade}] scanning: {url}")
        code = _download_from_url(url, args.max_pages, args.limit, out_dir)
        if code != 0:
            status = 1
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze and download files from Websiteedukasi pages")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a page and discover download links")
    analyze_parser.add_argument("url", help="Start URL")
    analyze_parser.add_argument("--max-pages", type=int, default=30, help="Maximum pages to scan")
    analyze_parser.add_argument("--output", help="Write analysis JSON to file")
    analyze_parser.set_defaults(func=cmd_analyze)

    download_parser = subparsers.add_parser("download", help="Analyze then download discovered files")
    download_parser.add_argument("url", help="Start URL")
    download_parser.add_argument("--max-pages", type=int, default=30, help="Maximum pages to scan")
    download_parser.add_argument("--limit", type=int, help="Download only the first N files")
    download_parser.add_argument("--out", default="downloads", help="Output directory")
    download_parser.set_defaults(func=cmd_download)

    download_classes_parser = subparsers.add_parser(
        "download-classes", help="Download modul files for multiple class URLs"
    )
    download_classes_parser.add_argument(
        "--classes", default="1-6", help='Class range/list, example: "1-6" or "1,2,4,5,6"'
    )
    download_classes_parser.add_argument("--exclude", default="", help='Exclude class list, example: "3"')
    download_classes_parser.add_argument("--max-pages", type=int, default=30, help="Maximum pages to scan")
    download_classes_parser.add_argument("--limit", type=int, help="Download only the first N files per class")
    download_classes_parser.add_argument("--out", default="downloads", help="Root output directory")
    download_classes_parser.set_defaults(func=cmd_download_classes)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
