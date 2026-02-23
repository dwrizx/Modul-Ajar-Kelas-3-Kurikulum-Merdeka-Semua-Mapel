# Changelog - Kelas 4 Rapikan + Dedup + Extract

Tanggal: 2026-02-24

## Tindakan
- Memindahkan arsip dari `downloads/kelas-4` ke struktur rapi `hasil_rapi_v2`.
- Menormalkan nama folder tujuan dari `4` menjadi `kelas-4`.
- Menjalankan deduplikasi + normalisasi + extract menggunakan:
  - `scripts/normalisasi_hasil_rapi.py`

## Hasil
- Arsip sumber: **139**
- Arsip unik setelah dedup: **23**
- Extract OK: **21**
- Extract FAIL: **2**
- Total file hasil extract: **166**

## Struktur Final
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-4/ganjil`
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-4/genap`
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-4/deep-learning`

## Verifikasi
- `downloads/kelas-4` sekarang tidak punya file `.rar`.
- Index dan ringkasan tersedia di:
  - `.../kelas-4/INDEX.md`
  - `.../kelas-4/RINGKASAN_RAPI.md`
  - `.../kelas-4/summary.json`
