# Changelog - 2026-02-24 - Script Rapi V2 Kelas 1

## Summary
Membuat script Python otomatis untuk merapikan hasil download kelas menjadi struktur `hasil_rapi_v2` yang lebih dangkal, dengan mode pindah (`move`) dan opsi ekstraksi.

## What Changed
- Menambahkan script:
  - `scripts/rapikan_hasil_kelas.py`
- Fitur utama script:
  - pindah arsip (bukan copy) ke struktur:
    - `kelas-X/ganjil/<mapel>/{arsip,extract}`
    - `kelas-X/genap/<mapel>/{arsip,extract}`
    - `kelas-X/deep-learning/<mapel>/{arsip,extract}`
  - ekstrak arsip ke folder `extract` dengan model flat (tanpa subfolder bertingkat).
  - timeout per arsip (`--timeout`) agar tidak hang.
  - mode cepat `--move-only` untuk hanya pindah arsip.
  - opsi `--include-root` untuk ikut merapikan `.rar` di root source.
  - output laporan:
    - `summary.json`
    - `INDEX.md`
    - `RINGKASAN_RAPI.md`

## Why
- Memenuhi kebutuhan struktur folder lebih ringkas dan mudah diautomasi.
- Menghindari folder bertingkat berlebihan dari hasil extract sebelumnya.
- Memastikan proses bisa dilanjutkan saat ada arsip lambat/rusak (timeout + mode move-only).

## Impact / Risk
- Impact:
  - `downloads/kelas-1` sudah dipindah ke target rapi `hasil_rapi_v2/kelas-1`.
  - struktur sekarang konsisten dan lebih mudah dipakai.
- Risk:
  - arsip rusak tetap bisa menghasilkan extract tidak lengkap jika mode ekstrak dipakai.
- Mitigation:
  - gunakan `--move-only` untuk perapian cepat, lalu ekstrak bertahap bila diperlukan.

## Testing Evidence
Verifikasi utama:
- `find downloads/kelas-1 -type f -name '*.rar' | wc -l` -> `0`
- `find /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-1 -type f -name '*.rar' | wc -l` -> `233`
- struktur target valid hingga level mapel + `arsip/extract`.

## Notes
- Contoh referensi yang dianalisis: `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2`.
