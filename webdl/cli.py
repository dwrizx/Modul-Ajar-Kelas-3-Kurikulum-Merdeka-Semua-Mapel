from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import requests

from .crawler import analyze_site
from .downloader import download_file


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
    report = analyze_site(args.url, max_pages=args.max_pages)
    if not report.direct_files:
        print("No direct file links found.")
        return 1

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; webdl/1.0)"})

    limit = args.limit if args.limit is not None else len(report.direct_files)
    selected = report.direct_files[:limit]

    out_dir = Path(args.out)
    for link in selected:
        try:
            output_path = download_file(session, link, out_dir)
            print(f"Downloaded: {output_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"Failed: {link} ({exc})")

    return 0


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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
