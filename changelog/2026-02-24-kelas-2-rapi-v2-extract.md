# Changelog - 2026-02-24 - Kelas 2 Rapi V2 + Extract

## Summary
Merapikan Kelas 2 ke format `hasil_rapi_v2` (move, bukan copy), lalu dedup dan ekstrak ulang agar struktur lebih bersih dan tidak berulang.

## What Changed
- Menjalankan:
  - `scripts/rapikan_hasil_kelas.py` untuk move + extract awal Kelas 2.
  - `scripts/normalisasi_hasil_rapi.py` untuk dedup struktur Kelas 2.
- Menjalankan extract pass-2 timeout-safe per arsip.
- Memperbarui:
  - `INDEX.md`
  - `RINGKASAN_RAPI.md`
  - `summary.json`
  pada `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-2`.

## Why
- Mengurangi duplikasi dan membuat struktur folder Kelas 2 lebih rapi serta konsisten dengan format v2.

## Impact / Risk
- Impact:
  - Arsip Kelas 2 pindah penuh ke target rapi.
  - Struktur mapel lebih bersih dan mudah dinavigasi.
- Risk:
  - Beberapa arsip tetap gagal ekstrak karena kualitas arsip sumber.

## Testing Evidence
- Arsip di source lama:
  - `downloads/kelas-2` -> `0` file `.rar`
- Arsip final di target:
  - `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-2` -> `17` arsip
- Extract pass-2:
  - `OK=13`
  - `FAIL=4`

## Notes
- Backup otomatis tersedia:
  - `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-2_before_dedup`
