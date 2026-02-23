# Changelog - Fix Nama Folder Output Kelas

Tanggal: 2026-02-24

## Masalah
- `scripts/rapikan_hasil_kelas.py` membuat folder output sesuai nilai mentah `--kelas`.
- Contoh `--kelas 4` menghasilkan folder `.../4`, bukan `.../kelas-4`.

## Perbaikan
- Menambahkan normalisasi argumen `--kelas`:
  - Jika input sudah `kelas-*`, pakai apa adanya.
  - Jika input angka/string biasa, otomatis jadi `kelas-<nilai>`.

## Dampak
- Struktur output jadi konsisten untuk semua run berikutnya.
- Mengurangi langkah rename manual setelah proses rapikan.

## File Diubah
- `scripts/rapikan_hasil_kelas.py`
