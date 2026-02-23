# python-donwload

Tool Python untuk menganalisis halaman Websiteedukasi, menemukan link file, mengunduh arsip, lalu merapikan hasil menjadi struktur folder yang konsisten per kelas/semester.

Project ini fokus pada workflow modul ajar SD/MI (kelas 1-6) dengan tiga kategori utama:
- `ganjil`
- `genap`
- `deep-learning`

Termasuk handling khusus untuk:
- link Google Drive dengan halaman konfirmasi,
- deduplikasi arsip,
- ekstraksi `.rar` dengan flatten output,
- laporan ringkas (`INDEX.md`, `RINGKASAN_RAPI.md`, `summary.json`).

## Fitur

- Crawl halaman modul dan turunan link internal.
- Klasifikasi link menjadi:
  - halaman modul,
  - halaman download,
  - direct file.
- Download file dengan penamaan aman.
- Handling Google Drive confirmation flow.
- Batch download kelas (`download-classes`).
- Rapikan hasil download ke struktur folder terstandar.
- Deduplikasi arsip (`name-size` atau `sha1`).
- Ekstraksi arsip dengan output flat (tanpa subfolder dalam).
- Ringkasan hasil per kelas.

## Struktur Project

```text
python-donwload/
├── webdl/
│   ├── cli.py
│   ├── crawler.py
│   ├── downloader.py
│   ├── extractor.py
│   └── models.py
├── scripts/
│   ├── rapikan_hasil_kelas.py
│   └── normalisasi_hasil_rapi.py
├── tests/
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_downloader.py
│   └── test_extractor.py
├── changelog/
├── analysis/
├── downloads/
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirement

- Python `>=3.14`
- `uv`
- `unar` (untuk ekstraksi `.rar`)

Cek `unar`:

```bash
unar -version
```

## Setup

```bash
uv sync
```

Jika cache default `uv` tidak writable:

```bash
UV_CACHE_DIR=.uv-cache uv sync
```

## CLI Utama (`webdl.cli`)

### 1) Analyze

```bash
uv run python -m webdl.cli analyze "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --output analysis-kelas3.json
```

Output:
- jumlah halaman discan,
- jumlah halaman modul,
- jumlah halaman download,
- jumlah direct files,
- daftar direct files.

Argumen:
- `url`: URL awal.
- `--max-pages`: batas jumlah halaman crawl.
- `--output`: file JSON hasil analisis.

### 2) Download (single class URL)

```bash
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --out downloads
```

Argumen:
- `url`: URL awal.
- `--max-pages`: batas crawl.
- `--limit`: batasi N file pertama.
- `--out`: folder output.

### 3) Download Kelas Sekaligus

```bash
uv run python -m webdl.cli download-classes --classes "1-6" --max-pages 30 --out downloads
```

Contoh exclude kelas tertentu:

```bash
uv run python -m webdl.cli download-classes --classes "1-6" --exclude "3" --max-pages 30 --out downloads
```

Argumen:
- `--classes`: range/list kelas. Contoh `1-6` atau `1,2,4,5,6`.
- `--exclude`: kelas yang dikecualikan.
- `--max-pages`: batas crawl per kelas.
- `--limit`: batas file per kelas.
- `--out`: root output download.

## Script Rapikan Hasil Download

### A) `scripts/rapikan_hasil_kelas.py`

Fungsi:
- memindahkan arsip dari `downloads/kelas-X` ke struktur rapi,
- optional ekstraksi langsung,
- membuat `INDEX.md`, `RINGKASAN_RAPI.md`, `summary.json`.

Dukungan alias penting:
- kategori `genjil` otomatis dipetakan ke `ganjil`,
- subject `pai-bp` otomatis dipetakan ke `pai`,
- `--kelas 4` otomatis jadi folder `kelas-4`.

Contoh (move only):

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/rapikan_hasil_kelas.py \
  --source downloads/kelas-4 \
  --target-root /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2 \
  --kelas 4 \
  --move-only
```

Contoh (move + extract):

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/rapikan_hasil_kelas.py \
  --source downloads/kelas-4 \
  --target-root /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2 \
  --kelas kelas-4 \
  --timeout 120
```

Argumen utama:
- `--source`: sumber folder kelas.
- `--target-root`: root hasil rapi.
- `--kelas`: nama/nomor kelas.
- `--move-only`: skip ekstraksi.
- `--timeout`: timeout ekstraksi per arsip.
- `--include-root`: ikut proses `.rar` di root source.
- `--quiet`: matikan progress log.

### B) `scripts/normalisasi_hasil_rapi.py`

Fungsi:
- normalisasi ulang struktur `kelas-X` yang sudah ada,
- deduplikasi arsip,
- klasifikasi ulang kategori/mapel,
- ekstraksi ulang (atau move only),
- simpan backup lama ke `kelas-X_before_dedup`.

Contoh:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/normalisasi_hasil_rapi.py \
  --kelas-dir /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-4 \
  --dedupe-mode name-size
```

Mode dedup:
- `name-size` (cepat, default)
- `sha1` (lebih ketat, lebih lambat)

Contoh move only:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/normalisasi_hasil_rapi.py \
  --kelas-dir /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-4 \
  --dedupe-mode sha1 \
  --move-only
```

## Struktur Output Rapi

Target struktur per kelas:

```text
hasil_rapi_v2/
└── kelas-6/
    ├── ganjil/
    │   └── <subject>/
    │       ├── arsip/
    │       └── extract/
    ├── genap/
    │   └── <subject>/
    │       ├── arsip/
    │       └── extract/
    └── deep-learning/
        └── <subject>/
            ├── arsip/
            └── extract/
```

Output laporan per kelas:
- `INDEX.md`: ringkasan jumlah arsip/extract per mapel.
- `RINGKASAN_RAPI.md`: ringkasan total proses.
- `summary.json`: detail item + status extract + error.

## Workflow End-to-End (Rekomendasi)

1. Download dari URL kelas:

```bash
UV_CACHE_DIR=.uv-cache uv run python -m webdl.cli download \
  "https://www.websiteedukasi.com/modul-ajar-kelas-6.html" \
  --max-pages 30 \
  --out downloads
```

2. Rapikan ke struktur target (move only):

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/rapikan_hasil_kelas.py \
  --source downloads/kelas-6 \
  --target-root /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2 \
  --kelas 6 \
  --move-only
```

3. Normalisasi + dedup + extract:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/normalisasi_hasil_rapi.py \
  --kelas-dir /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6 \
  --dedupe-mode name-size
```

4. Verifikasi hasil:

```bash
find /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6 -maxdepth 2 -type d | sort
sed -n '1,200p' /home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-6/INDEX.md
```

## Testing

Jalankan semua test:

```bash
UV_CACHE_DIR=.uv-cache uv run pytest -q
```

## Troubleshooting

### 1) `uv` cache permission error

Gunakan prefix ini di semua command:

```bash
UV_CACHE_DIR=.uv-cache
```

### 2) Extract `.rar` gagal

Kemungkinan:
- arsip source corrupt/partial,
- timeout ekstraksi,
- format arsip bermasalah.

Langkah:
- cek detail error di `summary.json`,
- naikkan `--timeout`,
- coba `--move-only` dulu untuk memisahkan masalah download vs ekstraksi.

### 3) Kategori tidak sesuai (`genap` masuk `ganjil`)

Jalankan normalisasi ulang:

```bash
UV_CACHE_DIR=.uv-cache uv run python scripts/normalisasi_hasil_rapi.py --kelas-dir <path-kelas>
```

Script normalisasi memakai sinyal nama file (mis. `Modul Ajar 2`, `Semester 2`) untuk recovery klasifikasi.

## Changelog Policy

Repo ini memakai workflow changelog aktif.

Setiap perubahan yang berdampak (fitur/behavior/CLI/script) wajib:
- update file di `changelog/`,
- menjelaskan: apa berubah, kenapa, dampak, verifikasi,
- sinkronkan docs terkait.

Referensi:
- `AGENTS.md`
- `skill/SKILL.md`
- `changelog/README.md`
- `changelog/_template.md`

## Catatan Legal

Gunakan tool ini secara bertanggung jawab:
- patuhi terms situs sumber,
- hormati hak cipta/lisensi dokumen,
- hindari crawling berlebihan yang membebani layanan.
