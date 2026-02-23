#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Candidate:
    path: Path
    dedup_key: str
    category: str
    subject: str
    score: int


def normalize_archive_name(name: str) -> str:
    n = name.lower().strip()
    # strip numeric suffix from previous collision renames: "file-2.rar"
    n = re.sub(r"-\d+\.rar$", ".rar", n)
    n = re.sub(r"\s+", " ", n)
    return n


def key_name_size(path: Path) -> str:
    st = path.stat()
    return f"{normalize_archive_name(path.name)}::{st.st_size}"


def sha1_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def infer_category(name: str, path: Path) -> str:
    n = name.lower()
    parts = [p.lower() for p in path.parts]
    if "deep learning" in n or "deep-learning" in n:
        return "deep-learning"
    if "deep-learning" in parts:
        return "deep-learning"
    # Filename signal should override path when recovering from previously mixed folders.
    if "semester 2" in n or re.search(r"\bmodul(\s+ajar)?\s*2\b", n):
        return "genap"
    # Trust explicit folder label when present in source tree.
    if "genap" in parts:
        return "genap"
    if "ganjil" in parts:
        return "ganjil"
    return "ganjil"


def infer_subject(name: str, path: Path, category: str) -> str:
    n = name.lower()
    parts = [p.lower() for p in path.parts]

    if "bahasa indonesia" in n or "b.indo" in n or "b indo" in n:
        return "bahasa-indonesia"
    if "bahasa inggris" in n or "b.inggris" in n or "b inggris" in n:
        return "bahasa-inggris"
    if "matematika" in n or " mtk " in f" {n} ":
        return "matematika"
    if "ipas" in n:
        return "ipas"
    if "pai" in n:
        return "pai"
    if "ppkn" in n or "pkn" in n or "pancasila" in n:
        return "pendidikan-pancasila" if category == "deep-learning" else "ppkn"
    if "pjok" in n:
        return "pjok"
    if "seni rupa" in n:
        return "seni-rupa" if category != "deep-learning" else "seni-rupa"
    if "seni tari" in n:
        return "seni-tari" if category != "deep-learning" else "seni-budaya"
    if "seni teater" in n:
        return "seni-teater" if category != "deep-learning" else "seni-budaya"
    if "seni musik" in n:
        return "seni-musik" if category != "deep-learning" else "seni-budaya"
    if "seni budaya" in n:
        return "seni-budaya"

    for p in parts:
        if p in {
            "bahasa-indonesia",
            "bahasa-inggris",
            "matematika",
            "ipas",
            "pai",
            "pjok",
            "ppkn",
            "seni-rupa",
            "seni-tari",
            "seni-teater",
            "seni-musik",
            "pendidikan-pancasila",
            "seni-budaya",
        }:
            return p

    return "arsip-lainnya"


def candidate_score(path: Path, category: str, subject: str) -> int:
    parts = [p.lower() for p in path.parts]
    score = 0
    if category in parts:
        score += 2
    if subject in parts:
        score += 2
    if "arsip" in parts:
        score += 1
    return score


def run_unar(archive: Path, out_dir: Path, timeout: int) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["unar", "-quiet", "-force-overwrite", "-output-directory", str(out_dir), str(archive)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, "unar not found"
    except subprocess.TimeoutExpired:
        return False, f"timeout > {timeout}s"
    if proc.returncode == 0:
        return True, ""
    msg = (proc.stderr or proc.stdout or "").strip()
    return False, msg[:500]


def unique_file_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    i = 2
    while True:
        c = path.with_name(f"{stem}-{i}{suffix}")
        if not c.exists():
            return c
        i += 1


def move_extract_flat(tmp_dir: Path, extract_dir: Path, tag: str) -> int:
    count = 0
    for src in tmp_dir.rglob("*"):
        if not src.is_file():
            continue
        dst = extract_dir / src.name
        if dst.exists():
            dst = unique_file_path(extract_dir / f"{src.stem}__{tag}{src.suffix}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalisasi hasil_rapi agar bebas duplikasi")
    parser.add_argument("--kelas-dir", required=True, help="Contoh: /home/.../hasil_rapi_v2/kelas-1")
    parser.add_argument("--timeout", type=int, default=90, help="Timeout unar per arsip")
    parser.add_argument("--move-only", action="store_true", help="Skip extract, hanya rapikan arsip")
    parser.add_argument(
        "--dedupe-mode",
        choices=["name-size", "sha1"],
        default="name-size",
        help="Mode deduplikasi: cepat (name-size) atau ketat (sha1)",
    )
    args = parser.parse_args()

    kelas_dir = Path(args.kelas_dir).resolve()
    if not kelas_dir.exists():
        raise SystemExit(f"kelas_dir not found: {kelas_dir}")

    build_dir = kelas_dir.with_name(kelas_dir.name + "_clean_tmp")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    rar_files = sorted(kelas_dir.rglob("*.rar"))
    by_hash: dict[str, Candidate] = {}
    source_total = len(rar_files)

    for rar in rar_files:
        if "_clean_tmp" in rar.parts:
            continue
        h = key_name_size(rar) if args.dedupe_mode == "name-size" else sha1_file(rar)
        cat = infer_category(rar.name, rar)
        sub = infer_subject(rar.name, rar, cat)
        score = candidate_score(rar, cat, sub)
        c = Candidate(path=rar, dedup_key=h, category=cat, subject=sub, score=score)
        old = by_hash.get(h)
        if old is None or c.score > old.score:
            by_hash[h] = c

    picked = list(by_hash.values())
    results = []
    for c in picked:
        target_subject = build_dir / c.category / c.subject
        arsip_dir = target_subject / "arsip"
        extract_dir = target_subject / "extract"
        arsip_dir.mkdir(parents=True, exist_ok=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        dst_archive = unique_file_path(arsip_dir / c.path.name)
        shutil.move(str(c.path), str(dst_archive))

        extracted = 0
        ok = True
        err = ""
        if not args.move_only:
            tmp_dir = extract_dir / f".tmp__{dst_archive.stem}"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            ok, err = run_unar(dst_archive, tmp_dir, args.timeout)
            extracted = move_extract_flat(tmp_dir, extract_dir, dst_archive.stem)
            shutil.rmtree(tmp_dir, ignore_errors=True)

        results.append(
            {
                "dedup_key": c.dedup_key,
                "category": c.category,
                "subject": c.subject,
                "archive": dst_archive.name,
                "source": str(c.path),
                "extract_status": "OK" if ok else "FAIL",
                "extracted_files": extracted,
                "error": err,
            }
        )

    # swap old -> backup, clean_tmp -> final
    backup = kelas_dir.with_name(kelas_dir.name + "_before_dedup")
    if backup.exists():
        shutil.rmtree(backup)
    kelas_dir.rename(backup)
    build_dir.rename(kelas_dir)

    # write reports
    ok = sum(1 for r in results if r["extract_status"] == "OK")
    fail = sum(1 for r in results if r["extract_status"] == "FAIL")
    extracted_total = sum(int(r["extracted_files"]) for r in results)
    summary = {
        "source_archives_found": source_total,
        "unique_archives_by_key": len(picked),
        "dedupe_mode": args.dedupe_mode,
        "extract_ok": ok,
        "extract_fail": fail,
        "extracted_files": extracted_total,
        "backup_dir": str(backup),
        "items": results,
    }
    (kelas_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    idx_lines = ["# Index Folder", ""]
    for cat in ["ganjil", "genap", "deep-learning"]:
        cat_dir = kelas_dir / cat
        if not cat_dir.exists():
            continue
        idx_lines.append(f"## {cat}")
        for subj in sorted([p for p in cat_dir.iterdir() if p.is_dir()]):
            ac = len(list((subj / "arsip").glob("*.rar"))) if (subj / "arsip").exists() else 0
            ec = len([p for p in (subj / "extract").glob("*") if p.is_file()]) if (subj / "extract").exists() else 0
            idx_lines.append(f"- {subj.name}: arsip={ac}, extract={ec}")
        idx_lines.append("")
    (kelas_dir / "INDEX.md").write_text("\n".join(idx_lines).rstrip() + "\n", encoding="utf-8")

    ringkas = [
        "# Ringkasan Rapi",
        "",
        f"- Arsip ditemukan: **{source_total}**",
        f"- Arsip unik ({args.dedupe_mode}): **{len(picked)}**",
        f"- Ekstrak OK: **{ok}**",
        f"- Ekstrak FAIL: **{fail}**",
        f"- Total file extract: **{extracted_total}**",
        "",
        f"- Backup lama: `{backup}`",
    ]
    (kelas_dir / "RINGKASAN_RAPI.md").write_text("\n".join(ringkas) + "\n", encoding="utf-8")

    print(f"DONE source={source_total} unique={len(picked)} backup={backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
