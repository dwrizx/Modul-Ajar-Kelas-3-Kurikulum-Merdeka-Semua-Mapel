# Changelog - 2026-02-24 - Kelas 1 Extract Rapi

## Summary
Melakukan ekstraksi arsip `.rar` Kelas 1 dan menata hasil ke struktur folder rapi per kategori.

## What Changed
- Ekstraksi ke `downloads/kelas-1/extracted-rapi/`.
- Struktur hasil:
  - `ganjil/`
  - `genap/`
  - `mendalam/`
  - `misc/root/` (arsip lama dari root)
- Ringkasan dibuat:
  - `downloads/kelas-1/extracted-rapi/_extract-summary.tsv`
  - `downloads/kelas-1/extracted-rapi/_extract-fail.tsv`
  - `downloads/kelas-1/extracted-rapi/_README.txt`

## Why
- Memenuhi permintaan ekstrak Kelas 1 dengan struktur folder lebih teratur.

## Impact / Risk
- Impact:
  - Hasil extract terorganisir dan mudah dicari.
- Risk:
  - Sebagian arsip gagal diekstrak penuh karena kualitas arsip sumber.
- Mitigation:
  - Menyimpan fail list dan log per arsip.

## Testing Evidence
- Total diproses: `233`
- `OK`: `136`
- `FAIL`: `97`
- Contoh error log: `Attempted to read more data than was available`

## Notes
- Ekstraksi menggunakan `unar`.
- Batch final mengecualikan folder hasil extract agar tidak terjadi loop pemrosesan ulang.
