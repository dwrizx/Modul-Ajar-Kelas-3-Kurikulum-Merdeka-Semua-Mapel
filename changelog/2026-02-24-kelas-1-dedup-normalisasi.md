# Changelog - 2026-02-24 - Kelas 1 Dedup dan Normalisasi Struktur

## Summary
Menyempurnakan proses perapian Kelas 1 agar lebih bersih, minim duplikasi, dan struktur folder lebih ringkas mengikuti pola `hasil_rapi_v2`.

## What Changed
- Menambahkan script:
  - `scripts/normalisasi_hasil_rapi.py`
- Menyempurnakan script:
  - dedup mode cepat `name-size`
  - normalisasi nama arsip untuk mengabaikan suffix duplikat (`-2`, `-3`, dst.)
  - kategori ditentukan dari nama file (menghindari kontaminasi dari path lama)
  - swap aman: versi lama dibackup otomatis ke `kelas-1_before_dedup`
- Menyempurnakan script sebelumnya:
  - `scripts/rapikan_hasil_kelas.py`
  - tambah `--move-only`, `--timeout`, `--include-root`
- Menjalankan normalisasi untuk:
  - `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-1`

## Why
- Mengurangi duplikasi arsip dan subfolder berlebihan pada Kelas 1.
- Membuat struktur lebih mudah dipakai untuk automasi selanjutnya.

## Impact / Risk
- Impact:
  - Struktur kelas-1 lebih ringkas dan konsisten.
  - Arsip unik turun ke set yang lebih masuk akal.
- Risk:
  - Beberapa arsip sumber tetap gagal ekstrak karena kualitas file sumber.
- Mitigation:
  - Daftar hasil extract OK/FAIL disimpan dan indeks diupdate.
  - Versi sebelum normalisasi disimpan sebagai backup.

## Testing Evidence
- Arsip di kelas-1 setelah normalisasi: `16` file (`*/arsip/*.rar`)
- Extract pass-2:
  - `OK=10`
  - `FAIL=6`
- Ringkasan terbarui:
  - `INDEX.md`
  - `RINGKASAN_RAPI.md`
  - `summary.json`

## Notes
- Backup otomatis:
  - `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-1_before_dedup`
