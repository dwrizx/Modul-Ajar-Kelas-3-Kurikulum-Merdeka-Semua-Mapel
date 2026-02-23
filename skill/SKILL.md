# skill.md — Maintainable Feature Change (Changelog + Docs + Log Review)

**Skill name:** maintainable_feature_change  
**Version:** 1.0  
**Scope:** engineering workflow / repo hygiene  
**Applies to:** semua perubahan fitur/behavior/API/CLI/config/UI yang berdampak ke user/dev  
**Owner:** {{NAME_OR_TEAM}}  
**Last updated:** {{YYYY-MM-DD}}

---

## 1) Tujuan

Skill ini memastikan setiap perubahan fitur:
- mudah dilacak (traceable),
- mudah dirawat (maintainable),
- dokumentasinya tidak ketinggalan,
- dan tidak mengulang kesalahan/keputusan lama karena tidak baca histori.

---

## 2) Kapan dipakai (Trigger)

Gunakan skill ini ketika ada:
- fitur baru
- perubahan behavior/alur
- perubahan API/CLI output/flag
- perubahan config/env yang mempengaruhi pengguna
- perubahan permission/auth/security
- perubahan UX/UI flow
- perubahan performa yang terasa user (cache, batching, limit, dsb.)

> Kalau ragu: anggap “fitur berubah” → pakai skill ini.

---

## 3) Input & Output

### Input yang dibutuhkan
- Path area kode yang akan diubah (folder/file/module)
- Konteks perubahan (bug/permintaan/optimasi)
- Status repo (branch, commit terbaru)
- Lokasi docs (README/docs/examples) dan folder changelog

### Output yang diharapkan
- ✅ 1 file changelog baru di `changelog/` (jika edit fitur)
- ✅ docs terkait terupdate (README/docs/examples/.env.example)
- ✅ catatan “Pre-Work Note” (minimal 3 poin: tujuan, dampak, docs yang diupdate)
- ✅ testing dilakukan (atau manual steps ditulis)
- ✅ perubahan siap direview & push

---

## 4) Aturan Wajib (Non-Negotiable)

1) **Pre-Work log review wajib** sebelum mulai coding  
2) **Setiap edit fitur wajib bikin changelog** di `changelog/yyyy-mm-dd-featurechange.md`  
3) **Sebelum push wajib update related docs**, bukan cuma changelog  
4) Changelog harus menjelaskan: *apa berubah, kenapa, dampaknya, testing*  
5) Perubahan harus dapat diuji (unit/integration/manual steps)

---

## 5) Workflow Langkah Demi Langkah (SOP)

### Step 0 — Pre-Work: Cek Log (WAJIB)
**Target waktu:** 5–10 menit

Checklist:
- [ ] Baca changelog terbaru di `changelog/` (3–10 file terakhir)
- [ ] Cek `git log` di area yang mau disentuh (10–30 commit terakhir)
- [ ] Baca docs terkait (README/docs/API/examples)
- [ ] Pahami “kontrak behavior” saat ini: input/output/error/config/side effect
- [ ] Cari tanda migrasi/refactor besar yang sedang berjalan

Command cepat (opsional):
```bash
ls -1 changelog | tail -n 10
git log --oneline -n 30 -- path/to/area
git blame -n path/to/file
rg -n "keyword|endpoint|flag" README.md docs/ examples/ 2>/dev/null
