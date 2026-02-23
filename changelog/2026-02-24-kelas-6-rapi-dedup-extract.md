# Changelog - Kelas 6 Rapikan + Dedup + Extract

Tanggal: 2026-02-24

## Tindakan
- Menjalankan rapikan awal dari `downloads/kelas-6` ke `hasil_rapi_v2/kelas-6`.
- Menemukan sisa arsip karena source menggunakan folder `genjil` (bukan `ganjil`).
- Memperbaiki script rapikan agar mendukung alias:
  - kategori `genjil` -> `ganjil`
  - subject `pai-bp` -> `pai`
- Menjalankan ulang rapikan untuk memindahkan sisa arsip.
- Menjalankan normalisasi + deduplikasi + ekstraksi:
  - `scripts/normalisasi_hasil_rapi.py`

## Hasil
- Arsip sumber: **163**
- Arsip unik setelah dedup: **19**
- Extract OK: **10**
- Extract FAIL: **9**
- Total file extract: **194**

## Struktur Final
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6/ganjil`
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6/genap`
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6/deep-learning`

## Verifikasi
- `downloads/kelas-6` sekarang tidak memiliki file `.rar`.
- Ringkasan dan index tersedia:
  - `.../kelas-6/INDEX.md`
  - `.../kelas-6/RINGKASAN_RAPI.md`
  - `.../kelas-6/summary.json`
