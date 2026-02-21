# python-donwload

Tool Python modular untuk:
- menganalisis halaman Websiteedukasi,
- menemukan link download file,
- mengunduh file otomatis,
- dan menata hasil unduhan agar rapi.

Proyek ini dibangun untuk workflow seperti `modul-ajar-kelas-3` (Ganjil, Genap, Deep Learning), termasuk handling link Google Drive yang butuh konfirmasi untuk file besar.

## Fitur Utama

- Analisis link bertahap dari halaman awal.
- Deteksi 3 jenis link:
  - halaman modul (`/modul-ajar-...`)
  - halaman download (`/download/...`)
  - file langsung (mis. Google Drive `export=download`)
- Download file otomatis ke folder target.
- Penamaan file otomatis dari:
  - `Content-Disposition`
  - query `id` (Google Drive)
  - nama path URL
- Support konfirmasi download Google Drive (halaman virus scan warning).
- Arsitektur modular agar mudah dikembangkan.
- Unit test untuk bagian ekstraksi dan downloader.

## Struktur Proyek

```text
python-donwload/
├── webdl/
│   ├── __init__.py
│   ├── cli.py          # CLI: analyze, download
│   ├── crawler.py      # Crawl halaman dan kumpulkan link
│   ├── downloader.py   # Download file + handling Google Drive
│   ├── extractor.py    # Ekstraksi URL dari HTML
│   └── models.py       # Dataclass model laporan
├── tests/
│   ├── conftest.py
│   ├── test_downloader.py
│   └── test_extractor.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirement

- Python `>=3.14`
- `uv` (package/dependency runner)

## Instalasi & Setup

1. Sinkronkan environment:

```bash
uv sync
```

2. (Opsional) jika cache `uv` di home tidak bisa ditulis, gunakan cache lokal proyek:

```bash
UV_CACHE_DIR=.uv-cache uv sync
```

## Cara Pakai CLI

### 1) Analyze halaman

```bash
uv run python -m webdl.cli analyze "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --output analysis-kelas3.json
```

Penjelasan argumen:
- `url`: URL awal yang mau dianalisis.
- `--max-pages`: batas jumlah halaman yang discan.
- `--output`: simpan laporan JSON.

Output terminal contoh:
- jumlah halaman yang discan
- jumlah halaman modul
- jumlah halaman download
- jumlah direct file
- daftar direct file

### 2) Download file

```bash
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --out downloads
```

Penjelasan argumen:
- `url`: URL awal.
- `--max-pages`: batas scan.
- `--limit`: batasi hanya N file pertama (opsional).
- `--out`: folder output file download.

Contoh batasi 3 file pertama:

```bash
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --limit 3 --out downloads
```

## Workflow Rekomendasi (Kasus Nyata Kelas 3)

Untuk hasil rapi per kategori:

- `ganjil/<mapel>/arsip`
- `ganjil/<mapel>/extract`
- `genap/<mapel>/arsip`
- `genap/<mapel>/extract`
- `deep-learning/<mapel>/arsip`
- `deep-learning/<mapel>/extract`

Flow praktis:
1. Analyze per halaman mapel.
2. Ambil halaman `/download/...` utama.
3. Ambil direct file dari halaman download.
4. Download ke folder `arsip`.
5. Extract ke folder `extract`.
6. Flatten isi `extract` (opsional) agar tanpa subfolder bertingkat.

## Arsitektur Modul

### `webdl/extractor.py`
Tanggung jawab:
- Parse HTML untuk atribut `href`, `src`, `action`.
- Normalisasi URL relatif ke absolut.
- Klasifikasi link menjadi:
  - `modul_pages`
  - `download_pages`
  - `direct_files`

Aturan direct file utama:
- extension file (`.pdf`, `.docx`, `.rar`, dll)
- Google Drive dengan query `export=download`

### `webdl/crawler.py`
Tanggung jawab:
- Crawl bertahap dari URL awal.
- Prioritaskan halaman download.
- Batasi scope domain dan halaman agar efisien.
- Keluarkan `AnalysisReport`.

### `webdl/downloader.py`
Tanggung jawab:
- Download file streaming (chunked write).
- Tentukan nama file aman.
- Handle kasus Google Drive warning page:
  - deteksi form konfirmasi
  - kirim request lanjutan otomatis

### `webdl/cli.py`
Tanggung jawab:
- Entry point command line (`analyze`, `download`).
- Menjembatani workflow analyzer + downloader.

### `webdl/models.py`
Berisi dataclass:
- `ExtractedLinks`
- `AnalysisReport`

## Testing

Jalankan semua test:

```bash
uv run pytest -q
```

Jika ada masalah cache `uv`:

```bash
UV_CACHE_DIR=.uv-cache uv run pytest -q
```

## Troubleshooting

### 1) `uv` gagal akses cache home
Error contoh: permission denied di `~/.cache/uv`

Solusi:

```bash
UV_CACHE_DIR=.uv-cache uv run <command>
```

### 2) File Google Drive terdownload jadi HTML, bukan arsip
Biasanya terjadi karena halaman konfirmasi “Download anyway”.

Status saat ini:
- Downloader sudah include logic konfirmasi Google Drive.
- Jika masih terjadi, cek apakah link berubah format atau butuh cookie tambahan.

### 3) Extract `.rar` gagal
Kemungkinan:
- extractor tidak support varian RAR tertentu,
- arsip korup/tidak lengkap,
- nama/path dalam arsip aneh.

Solusi:
- coba tool extractor lain (`unar`, `7z`, `unrar`) sesuai environment,
- validasi isi arsip dengan listing dulu,
- cek ukuran file unduhan sesuai ekspektasi.

## Catatan Etika & Legal

Gunakan tool ini secara bertanggung jawab:
- patuhi Terms of Service website sumber,
- hormati hak cipta dan lisensi dokumen,
- jangan gunakan untuk scraping berlebihan yang merugikan layanan.

## Roadmap Pengembangan (Opsional)

- Tambah mode output CSV/Excel.
- Tambah retry + backoff lebih granular.
- Tambah checksum verification.
- Tambah parallel download terkontrol.
- Tambah command khusus `organize` untuk auto rapikan extract.

## Ringkas Command

```bash
# setup
uv sync

# analyze
uv run python -m webdl.cli analyze "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --output analysis-kelas3.json

# download
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --out downloads

# test
uv run pytest -q
```

Jika environment membatasi cache `uv`, prepend semua command dengan `UV_CACHE_DIR=.uv-cache`.
