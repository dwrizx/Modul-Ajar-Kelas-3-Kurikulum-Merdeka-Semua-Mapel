#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MoveResult:
    category: str
    subject: str
    source: str
    archive: str
    moved_to: str
    extract_status: str
    extracted_files: int
    error: str = ""


CATEGORY_MAP = {
    "ganjil": "ganjil",
    "genjil": "ganjil",
    "genap": "genap",
    "mendalam": "deep-learning",
}


SUBJECT_ALIAS = {
    "pkn": "ppkn",
    "ppkn": "ppkn",
    "pai-bp": "pai",
}


def normalize_subject(raw: str, category: str) -> str:
    s = raw.strip().lower()
    s = SUBJECT_ALIAS.get(s, s)
    if category == "mendalam" and s == "ppkn":
        return "pendidikan-pancasila"
    return s


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    i = 2
    while True:
        candidate = path.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def run_unar(archive: Path, out_dir: Path, timeout_seconds: int) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["unar", "-quiet", "-force-overwrite", "-output-directory", str(out_dir), str(archive)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        return False, "unar command not found"
    except subprocess.TimeoutExpired:
        return False, f"unar timeout > {timeout_seconds}s"
    if proc.returncode == 0:
        return True, ""
    err = (proc.stderr or proc.stdout or "").strip()
    return False, err[:500]


def move_extracted_files_flat(tmp_dir: Path, extract_dir: Path, archive_slug: str) -> int:
    moved = 0
    for src in tmp_dir.rglob("*"):
        if not src.is_file():
            continue
        dst = extract_dir / src.name
        if dst.exists():
            dst = unique_path(extract_dir / f"{src.stem}__{archive_slug}{src.suffix}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        moved += 1
    return moved


def process_category(
    src_root: Path,
    dst_root: Path,
    category: str,
    results: list[MoveResult],
    timeout_seconds: int,
    move_only: bool,
    verbose: bool = True,
) -> None:
    src_cat = src_root / category
    if not src_cat.exists():
        return

    dst_cat = dst_root / CATEGORY_MAP[category]
    dst_cat.mkdir(parents=True, exist_ok=True)

    for subject_dir in sorted([p for p in src_cat.iterdir() if p.is_dir()]):
        raw_subject = subject_dir.name
        subject = normalize_subject(raw_subject, category)
        rar_files = sorted(subject_dir.glob("*.rar"))
        if not rar_files:
            continue

        target_subject = dst_cat / subject
        arsip_dir = target_subject / "arsip"
        extract_dir = target_subject / "extract"
        arsip_dir.mkdir(parents=True, exist_ok=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        for rar in rar_files:
            dst_archive = unique_path(arsip_dir / rar.name)
            shutil.move(str(rar), str(dst_archive))

            archive_slug = dst_archive.stem.lower().replace(" ", "-")
            extracted_count = 0
            err = ""
            if move_only:
                ok = True
            else:
                tmp_extract = extract_dir / f".tmp__{archive_slug}"
                tmp_extract.mkdir(parents=True, exist_ok=True)
                ok, err = run_unar(dst_archive, tmp_extract, timeout_seconds)
                extracted_count = move_extracted_files_flat(tmp_extract, extract_dir, archive_slug)
                shutil.rmtree(tmp_extract, ignore_errors=True)

            results.append(
                MoveResult(
                    category=category,
                    subject=subject,
                    source=str(rar),
                    archive=dst_archive.name,
                    moved_to=str(dst_archive),
                    extract_status="OK" if ok else "FAIL",
                    extracted_files=extracted_count,
                    error=err,
                )
            )
            if verbose:
                mode = "MOVE" if move_only else "EXTRACT"
                print(
                    f"[{category}/{subject}] {dst_archive.name} -> {('OK' if ok else 'FAIL')} {mode} ({extracted_count} files)"
                )


def guess_subject_from_filename(name: str) -> str:
    n = name.lower()
    if "deep learning" in n:
        if "pancasila" in n or "ppkn" in n:
            return "pendidikan-pancasila"
        if "seni" in n:
            return "seni-budaya"
        if "matematika" in n or "mtk" in n:
            return "matematika"
        if "inggris" in n:
            return "bahasa-inggris"
        if "indonesia" in n:
            return "bahasa-indonesia"
        return "deep-learning-lainnya"
    if "pjok" in n:
        return "pjok"
    if "ppkn" in n or "pkn" in n:
        return "ppkn"
    if "pai" in n:
        return "pai"
    if "matematika" in n or "mtk" in n:
        return "matematika"
    if "inggris" in n:
        return "bahasa-inggris"
    if "indonesia" in n:
        return "bahasa-indonesia"
    if "seni rupa" in n:
        return "seni-rupa"
    if "seni tari" in n:
        return "seni-tari"
    if "seni teater" in n:
        return "seni-teater"
    if "seni musik" in n:
        return "seni-musik"
    return "arsip-lainnya"


def process_root_archives(
    src_root: Path, dst_root: Path, results: list[MoveResult], timeout_seconds: int, move_only: bool, verbose: bool
) -> None:
    root_rars = sorted(src_root.glob("*.rar"))
    if not root_rars:
        return

    for rar in root_rars:
        if "deep learning" in rar.name.lower():
            out_category = "deep-learning"
        else:
            out_category = "ganjil"
        out_subject = guess_subject_from_filename(rar.name)

        target_subject = dst_root / out_category / out_subject
        arsip_dir = target_subject / "arsip"
        extract_dir = target_subject / "extract"
        arsip_dir.mkdir(parents=True, exist_ok=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        dst_archive = unique_path(arsip_dir / rar.name)
        shutil.move(str(rar), str(dst_archive))

        archive_slug = dst_archive.stem.lower().replace(" ", "-")
        extracted_count = 0
        err = ""
        if move_only:
            ok = True
        else:
            tmp_extract = extract_dir / f".tmp__{archive_slug}"
            tmp_extract.mkdir(parents=True, exist_ok=True)
            ok, err = run_unar(dst_archive, tmp_extract, timeout_seconds)
            extracted_count = move_extracted_files_flat(tmp_extract, extract_dir, archive_slug)
            shutil.rmtree(tmp_extract, ignore_errors=True)

        results.append(
            MoveResult(
                category="root",
                subject=out_subject,
                source=str(rar),
                archive=dst_archive.name,
                moved_to=str(dst_archive),
                extract_status="OK" if ok else "FAIL",
                extracted_files=extracted_count,
                error=err,
            )
        )
        if verbose:
            mode = "MOVE" if move_only else "EXTRACT"
            print(f"[root/{out_subject}] {dst_archive.name} -> {('OK' if ok else 'FAIL')} {mode} ({extracted_count} files)")


def write_reports(out_class_dir: Path, results: list[MoveResult]) -> None:
    summary_json = out_class_dir / "summary.json"
    summary_md = out_class_dir / "RINGKASAN_RAPI.md"
    index_md = out_class_dir / "INDEX.md"

    ok = sum(1 for r in results if r.extract_status == "OK")
    fail = sum(1 for r in results if r.extract_status == "FAIL")
    total_files = sum(r.extracted_files for r in results)

    payload = {
        "archives_processed": len(results),
        "extract_ok": ok,
        "extract_fail": fail,
        "extracted_files": total_files,
        "items": [r.__dict__ for r in results],
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    summary_md.write_text(
        "\n".join(
            [
                "# Ringkasan Rapi",
                "",
                f"- Arsip diproses: **{len(results)}**",
                f"- Ekstrak OK: **{ok}**",
                f"- Ekstrak FAIL: **{fail}**",
                f"- Total file hasil extract: **{total_files}**",
                "",
                "## Struktur",
                "- `ganjil/<mapel>/arsip`",
                "- `ganjil/<mapel>/extract`",
                "- `genap/<mapel>/arsip`",
                "- `genap/<mapel>/extract`",
                "- `deep-learning/<mapel>/arsip`",
                "- `deep-learning/<mapel>/extract`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    lines = ["# Index Folder", ""]
    for cat in ["ganjil", "genap", "deep-learning"]:
        cat_dir = out_class_dir / cat
        if not cat_dir.exists():
            continue
        lines.append(f"## {cat}")
        for subject_dir in sorted([p for p in cat_dir.iterdir() if p.is_dir()]):
            arsip_count = len(list((subject_dir / "arsip").glob("*.rar"))) if (subject_dir / "arsip").exists() else 0
            extract_count = len([p for p in (subject_dir / "extract").glob("*") if p.is_file()]) if (
                subject_dir / "extract"
            ).exists() else 0
            lines.append(f"- {subject_dir.name}: arsip={arsip_count}, extract={extract_count}")
        lines.append("")
    index_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rapikan hasil download kelas dengan move + extract flat")
    parser.add_argument("--source", required=True, help="Path sumber kelas, contoh: downloads/kelas-1")
    parser.add_argument(
        "--target-root",
        required=True,
        help="Root output rapi v2, contoh: /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2",
    )
    parser.add_argument("--kelas", required=True, help='Nama kelas output, contoh: "kelas-1" atau "4"')
    parser.add_argument("--quiet", action="store_true", help="Matikan log progress")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout unar per arsip (detik)")
    parser.add_argument("--move-only", action="store_true", help="Hanya pindah arsip ke folder rapi, tanpa ekstrak")
    parser.add_argument("--include-root", action="store_true", help="Ikut rapikan file .rar yang ada di root source")
    args = parser.parse_args()

    src_root = Path(args.source).resolve()
    out_root = Path(args.target_root).resolve()
    kelas_raw = args.kelas.strip().lower()
    kelas_name = kelas_raw if kelas_raw.startswith("kelas-") else f"kelas-{kelas_raw}"
    out_class_dir = out_root / kelas_name
    out_class_dir.mkdir(parents=True, exist_ok=True)

    results: list[MoveResult] = []
    for cat in ["ganjil", "genjil", "genap", "mendalam"]:
        process_category(
            src_root,
            out_class_dir,
            cat,
            results,
            timeout_seconds=args.timeout,
            move_only=args.move_only,
            verbose=not args.quiet,
        )
    if args.include_root:
        process_root_archives(
            src_root,
            out_class_dir,
            results,
            timeout_seconds=args.timeout,
            move_only=args.move_only,
            verbose=not args.quiet,
        )

    write_reports(out_class_dir, results)
    print(f"DONE archives={len(results)} output={out_class_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
