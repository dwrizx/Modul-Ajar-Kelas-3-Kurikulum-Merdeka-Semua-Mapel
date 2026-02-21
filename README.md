# python-donwload

Downloader modular untuk menganalisis halaman Websiteedukasi lalu mengunduh file secara otomatis.

## Struktur

- `webdl/extractor.py`: ekstraksi link modul, link halaman download, dan link file langsung.
- `webdl/crawler.py`: crawl bertahap dari halaman awal untuk mengumpulkan target unduhan.
- `webdl/downloader.py`: download file (termasuk handling konfirmasi Google Drive file besar).
- `webdl/cli.py`: command line interface (`analyze` dan `download`).
- `tests/`: unit test extractor/downloader.

## Pakai

```bash
uv run python -m webdl.cli analyze "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --output analysis-kelas3.json
uv run python -m webdl.cli download "https://www.websiteedukasi.com/modul-ajar-kelas-3.html" --max-pages 30 --out downloads
```
