# Changelog - 2026-02-23 - Agents Changelog Policy

## Summary
Menambahkan kebijakan wajib changelog di `AGENTS.md`, serta membuat panduan dan template changelog agar alur kerja agent selalu membaca histori perubahan dan menulis changelog secara konsisten.

## What Changed
- Menambahkan section `Start Here (Read First)` di `AGENTS.md` agar agent:
  - membaca changelog terbaru saat membuka panduan,
  - membaca `skill/SKILL.md`,
  - menyelesaikan pre-work log review sebelum implementasi.
- Menambahkan section `Mandatory Changelog Policy` di `AGENTS.md` yang mewajibkan:
  - kapan changelog wajib dibuat,
  - format nama file changelog,
  - isi minimum changelog,
  - completion gate (pekerjaan belum selesai kalau changelog belum ditulis).
- Menambahkan referensi resmi di `AGENTS.md`:
  - `changelog/README.md`
  - `changelog/_template.md`
- Menambahkan file baru `changelog/README.md` sebagai panduan singkat penggunaan changelog.
- Menambahkan file baru `changelog/_template.md` sebagai format baku entry changelog.

## Why
- Memastikan histori perubahan selalu terdokumentasi dan mudah ditelusuri.
- Menyamakan aturan repo dengan workflow `maintainable_feature_change` di `skill/SKILL.md`.
- Mengurangi risiko perubahan tanpa konteks (kenapa diubah, dampak, dan bukti test tidak tercatat).

## Impact / Risk
- Impact:
  - Proses kerja agent jadi lebih disiplin dan konsisten.
  - Review dan handover lebih mudah karena setiap perubahan punya catatan.
- Risk:
  - Sedikit menambah langkah administratif saat menyelesaikan task.
- Mitigation:
  - Disediakan template dan panduan agar penulisan changelog cepat dan seragam.

## Testing Evidence
Commands run:

```bash
rg -n "Start Here|Mandatory Changelog Policy|changelog/_template.md|changelog/README.md" AGENTS.md
sed -n '1,220p' changelog/README.md
sed -n '1,220p' changelog/_template.md
```

Result:
- Seluruh section baru terdeteksi di `AGENTS.md`.
- `changelog/README.md` dan `changelog/_template.md` terbaca dengan isi sesuai kebijakan yang diinginkan.

## Notes
- Perubahan ini bersifat dokumentasi/proses; tidak mengubah runtime behavior aplikasi.
