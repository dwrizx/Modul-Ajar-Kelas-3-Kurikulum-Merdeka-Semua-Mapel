# Changelog - Refresh README Panduan Lengkap

Tanggal: 2026-02-24

## Apa yang berubah
- `README.md` ditulis ulang secara menyeluruh.
- Menambahkan dokumentasi detail untuk:
  - fitur utama,
  - struktur project,
  - command CLI (`analyze`, `download`, `download-classes`),
  - script rapikan (`rapikan_hasil_kelas.py`),
  - script normalisasi dedup (`normalisasi_hasil_rapi.py`),
  - workflow end-to-end kelas,
  - struktur output final,
  - troubleshooting,
  - kebijakan changelog.

## Kenapa diubah
- Dokumentasi lama belum mencakup alur aktual yang dipakai sekarang (rapikan + dedup + extract).
- Perlu panduan operasional yang bisa langsung dipakai untuk kelas 1-6.

## Dampak
- Onboarding lebih cepat.
- Eksekusi pipeline jadi konsisten.
- Mengurangi salah penggunaan argumen script.

## Verifikasi
- Review manual isi `README.md` terhadap implementasi di:
  - `webdl/cli.py`
  - `scripts/rapikan_hasil_kelas.py`
  - `scripts/normalisasi_hasil_rapi.py`
