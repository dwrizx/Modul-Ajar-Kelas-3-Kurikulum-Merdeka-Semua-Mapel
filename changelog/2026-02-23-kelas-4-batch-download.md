# Changelog - 2026-02-23 - Kelas 4 Batch Download

## Summary
Menjalankan batch `analyze + download` untuk Kelas 4 dengan struktur folder `ganjil`, `genap`, dan `mendalam`, lalu melakukan retry pada satu URL yang sempat timeout.

## What Changed
- Menjalankan analisis induk:
  - `analysis-kelas4-latest.json`
- Menjalankan `analyze + download` per URL Kelas 4 yang ditemukan dari halaman induk.
- Menyimpan output terstruktur:
  - `downloads/kelas-4/{ganjil,genap,mendalam}/...`
  - `analysis/kelas-4/{ganjil,genap,mendalam}/*.json`
- Menyimpan ringkasan batch:
  - `downloads/kelas-4/_summary.tsv`
- Menyimpan hasil retry:
  - `downloads/kelas-4/_retry.tsv`

## Why
- Menindaklanjuti permintaan download Kelas 4 dengan pola yang sama seperti batch kelas sebelumnya.
- Menjaga output tetap rapi dan bisa diaudit.

## Impact / Risk
- Impact:
  - Dataset Kelas 4 siap dipakai dengan struktur konsisten.
- Risk:
  - Satu URL sempat gagal karena `Read timed out` pada percobaan pertama.
- Mitigation:
  - Retry manual untuk URL tersebut berhasil.

## Testing Evidence
Commands run:

```bash
awk -F'\t' 'BEGIN{aok=0;af=0;dok=0;df=0} {if($1=="OK")aok++; else af++; if($2=="OK")dok++; else df++} END{printf "ANALYZE_OK=%d\nANALYZE_FAIL=%d\nDOWNLOAD_OK=%d\nDOWNLOAD_FAIL=%d\n",aok,af,dok,df}' downloads/kelas-4/_summary.tsv
find downloads/kelas-4 -type f ! -name '_download.log' ! -name '_analyze.log' ! -name '_summary.tsv' | wc -l
du -sh downloads/kelas-4
find downloads/kelas-4 -type f -size 0 | wc -l
```

Result:
- `ANALYZE_OK=23`
- `ANALYZE_FAIL=0`
- `DOWNLOAD_OK=22`
- `DOWNLOAD_FAIL=1` (status batch awal)
- Retry status: `OK` di `downloads/kelas-4/_retry.tsv` untuk `ganjil/matematika`
- Total file download: `139`
- Total ukuran: `1.8G`
- File 0 byte: `0`

## Notes
- Kegagalan awal `ganjil/matematika` disebabkan timeout jaringan sementara, bukan karena link tidak valid.
