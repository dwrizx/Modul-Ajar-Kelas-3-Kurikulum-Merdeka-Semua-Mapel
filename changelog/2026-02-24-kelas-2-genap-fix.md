# Changelog - Perbaikan Kelas 2 Genap Hilang

Tanggal: 2026-02-24

## Masalah
- Folder `genap` pada `hasil_rapi_v2/kelas-2` tidak muncul.
- Arsip `Modul Ajar 2 ...` salah masuk ke `ganjil`.

## Akar Penyebab
- Hasil normalisasi lama mengklasifikasikan arsip berdasarkan path yang sudah terlanjur berada di `ganjil`.
- Aturan inferensi kategori belum dipakai ulang pada struktur existing setelah patch terakhir.

## Tindakan
- Menjalankan ulang normalisasi kelas 2 dengan script terbaru:
  - `scripts/normalisasi_hasil_rapi.py`
- Verifikasi ulang struktur folder, `INDEX.md`, dan daftar arsip semester 2.

## Hasil
- Folder `genap` berhasil terbentuk kembali.
- Arsip `Modul Ajar 2 ...` sudah berada di:
  - `kelas-2/genap/<subject>/arsip/*.rar`
- `INDEX.md` kini menampilkan section `ganjil`, `genap`, `deep-learning` lengkap.

## Lokasi Terkait
- `/home/hades/2026-ramadhan/python-donwload/hasil_rapi_v2/kelas-2`
- `scripts/normalisasi_hasil_rapi.py`
