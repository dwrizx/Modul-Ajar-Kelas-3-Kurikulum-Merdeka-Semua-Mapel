# Changelog - 2026-02-24 - Kelas 5 Batch Download

## Summary
Menjalankan batch otomatis Kelas 5 dengan pola yang sama seperti kelas sebelumnya: analisis halaman induk, pengelompokan link ke `ganjil/genap/mendalam`, lalu `analyze + download` per link.

## What Changed
- Menjalankan analisis induk:
  - `analysis-kelas5-latest.json`
- Menjalankan batch `analyze + download` untuk 20 URL valid Kelas 5.
- Menyimpan output:
  - download: `downloads/kelas-5/{ganjil,genap,mendalam}/...`
  - analisis per link: `analysis/kelas-5/{ganjil,genap,mendalam}/*.json`
- Menyimpan ringkasan batch:
  - `downloads/kelas-5/_summary.tsv`

## Why
- Menindaklanjuti permintaan download Kelas 5 dengan struktur dan workflow konsisten.
- Memastikan data Kelas 5 siap dipakai dengan jejak status yang jelas.

## Impact / Risk
- Impact:
  - Semua link valid Kelas 5 berhasil dianalisis dan diunduh.
- Risk:
  - Ketergantungan ke stabilitas jaringan/sumber tetap ada.
- Mitigation:
  - Menyimpan log per item (`_analyze.log` dan `_download.log`) untuk retry jika sewaktu-waktu ada kegagalan.

## Testing Evidence
Commands run:

```bash
find downloads/kelas-5 -type f ! -name '_download.log' ! -name '_analyze.log' ! -name '_summary.tsv' | wc -l
du -sh downloads/kelas-5
find analysis/kelas-5 -type f -name '*.json' | wc -l
```

Result:
- `ANALYZE_OK=20`
- `ANALYZE_FAIL=0`
- `DOWNLOAD_OK=20`
- `DOWNLOAD_FAIL=0`
- Total file download: `21`
- Total ukuran: `270M`
- Total file analisis JSON: `20`

## Notes
- Ringkasan status detail tersimpan di `downloads/kelas-5/_summary.tsv`.
