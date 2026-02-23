# Changelog - 2026-02-23 - Kelas 2 Batch Analyze and Download

## Summary
Menjalankan proses `analyze + download` untuk paket Kelas 2 dengan struktur folder seperti Kelas 1 (`ganjil`, `genap`, `mendalam`), lalu melakukan koreksi URL berdasarkan hasil analisis halaman induk Kelas 2.

## What Changed
- Menjalankan batch awal 24 URL Kelas 2 ke:
  - `downloads/kelas-2/{ganjil,genap,mendalam}/...`
  - `analysis/kelas-2/{ganjil,genap,mendalam}/*.json`
- Menyimpan rekap status di:
  - `downloads/kelas-2/_summary.tsv`
- Menjalankan batch koreksi untuk URL valid tambahan:
  - `genap/pjok-semester-2`
  - `mendalam/bahasa-indonesia`
  - `mendalam/seni-rupa`
- Menyimpan analisis induk terbaru:
  - `analysis-kelas2-latest.json`

## Why
- Menyamakan pola kerja Kelas 2 dengan Kelas 1 (struktur rapi per kategori + output analisis).
- Memastikan URL yang dipakai sesuai tautan yang benar-benar tersedia pada halaman induk Kelas 2.

## Impact / Risk
- Impact:
  - Data Kelas 2 tersusun konsisten dan siap dipakai.
  - Tersedia jejak status sukses/gagal per URL.
- Risk:
  - Beberapa URL kategori seni tidak menyediakan file langsung dari sumber.
- Mitigation:
  - URL gagal tetap dicatat sebagai `DOWNLOAD_FAIL` dengan log yang jelas.
  - URL valid pengganti dijalankan lewat batch koreksi.

## Testing Evidence
Commands run:

```bash
awk -F'\t' 'BEGIN{aok=0;af=0;dok=0;df=0} {if($1=="OK")aok++; else af++; if($2=="OK")dok++; else df++} END{printf "ANALYZE_OK=%d\nANALYZE_FAIL=%d\nDOWNLOAD_OK=%d\nDOWNLOAD_FAIL=%d\n",aok,af,dok,df}' downloads/kelas-2/_summary.tsv
find downloads/kelas-2 -type f ! -name '_download.log' ! -name '_analyze.log' ! -name '_summary.tsv' | wc -l
du -sh downloads/kelas-2
find analysis/kelas-2 -type f -name '*.json' | wc -l
```

Result:
- `ANALYZE_OK=27`
- `ANALYZE_FAIL=0`
- `DOWNLOAD_OK=18`
- `DOWNLOAD_FAIL=9` (URL sumber tidak menyediakan direct file)
- Total file hasil download: `99`
- Total size: `813M`
- Total file analisis JSON: `27`

## Notes
- Kegagalan download yang tercatat berasal dari URL dengan hasil analisis `Direct files: 0`, bukan error jaringan.
