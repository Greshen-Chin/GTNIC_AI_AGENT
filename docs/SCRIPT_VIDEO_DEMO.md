# 🎬 SCRIPT & STORYBOARD VIDEO DEMO (3–5 MENIT)
## GTNIC SOAR — Garda Tech National Innovation Competition 2026
**Kategori:** AI Agent Development  
**Sub-Tema:** Building Intelligent AI Agents for Enterprise Productivity  
**Target Durasi:** 3 Menit 30 Detik – 4 Menit (Sesuai batas resmi 3–5 menit)  
**Media Upload:** YouTube (Unlisted atau Public) atau Google Drive (Akses Publik / Anyone with link)

---

## 🎯 STRATEGI & TIPS REKAMAN
1. **Resolusi Rekaman:** Minimal 1080p (Full HD), audio jernih (gunakan headset/mic eksternal).
2. **Tab Browser yang Disiapkan Sebelum Rekam:**
   - **Tab 1:** Slide Pembuka (Canva / Google Slides / PDF Proposal)
   - **Tab 2:** Live Dashboard SOC: `https://gtnic-hackwitgoh.vercel.app/`
   - **Tab 3:** Live Juice Shop Lab: `https://juice.flummox.cloud/`
   - **Tab 4:** Postman / Terminal / Browser URL bar (untuk trigger serangan)
   - **Tab 5:** Discord Channel Tim (untuk melihat bot notifikasi)
   - **Tab 6:** Repositori GitHub / Arsitektur sistem
3. **Tone Penyampaian:** Percaya diri, lugas, profesional (*authoritative & persuasive*), tempo berbicara sedang.

---

## ⏱️ RUNDOWN & STORYBOARD DETIK-DEMI-DETIK

```
+----------------------------------------------------------------------------------------------------+
| 00:00 - 00:30 (30d) | Scene 1: Pembukaan, Perkenalan Tim, & Problem Statement (PDN + BSSN)        |
| 00:30 - 01:05 (35d) | Scene 2: Solusi GTNIC SOAR & Arsitektur Autonomous Agent                    |
| 01:05 - 02:40 (95d) | Scene 3: LIVE DEMO PENYERANGAN & RESPON OTONOM AGENT (Bagian Paling Kritis) |
| 02:40 - 03:20 (40d) | Scene 4: Bukti Anti-Halusinasi, RAG MITRE/OWASP, & Human-in-the-Loop        |
| 03:20 - 03:45 (25d) | Scene 5: Dampak Bisnis (IBM Data) & Penutup                                  |
+----------------------------------------------------------------------------------------------------+
```

---

### SCENE 1: PEMBUKAAN & LATAR BELAKANG MASALAH (00:00 – 00:30)
* **Visual:**
  - Tampilkan Slide Judul: Logo GTNIC 2026, Nama Tim, Nama Anggota, Judul Karya: **GTNIC SOAR**.
  - Tampilkan grafis atau teks: *5,5 Miliar Serangan Siber BSSN 2025* | *Insiden Ransomware PDN Juni 2024* | *Defisit 4,8 Juta Tenaga Siber*.
* **Voiceover / Naskah:**
  > *"Halo Dewan Juri Garda Tech National Innovation Competition 2026. Kami dari Tim [Nama Tim] dengan bangga mempersembahkan **GTNIC SOAR: Autonomous AI SOC Agent for Enterprise Cybersecurity**.*
  >
  > *Tahukah Anda bahwa sepanjang tahun 2025, BSSN mencatat lebih dari 5,5 miliar anomali serangan siber di Indonesia—melonjak 714 persen? Serangan ransomware Pusat Data Nasional pada Juni 2024 yang melumpuhkan 282 layanan publik membuktikan bahwa pertahanan siber manual sudah tidak mampu mengejar laju serangan.*
  >
  > *Di saat yang sama, dunia mengalami kekurangan 4,8 juta profesional keamanan siber, dan 71 persen analis SOC mengalami burnout akibat kelelahan meneliti ribuan alert setiap hari. Inilah masalah yang kami selesaikan."*

---

### SCENE 2: PENGENALAN SOLUSI & ARSITEKTUR OTONOM (00:30 – 01:05)
* **Visual:**
  - Tampilkan diagram arsitektur sistem GTNIC SOAR (bisa dari slide atau gambar arsitektur).
  - Sorot komponen utama: *Telemetry Stream → Gemini 3.8 Flash Function Calling Loop → 4 Investigasi Tools → Anti-Hallucination Guard → Next.js Dashboard*.
* **Voiceover / Naskah:**
  > *"GTNIC SOAR bukan sekadar chatbot atau wrapper LLM sederhana. Kami membangun agen keamanan otonom berbasis model fondasi Gemini 3.8 Flash pada Google Cloud Vertex AI yang mampu berpikir, merencanakan, dan mengeksekusi investigasi forensik secara mandiri.*
  >
  > *Agen ini dibekali empat perkakas digital: inspeksi payload web, pencarian riwayat anomali IP pada SIEM Wazuh, analisis anomali autentikasi, serta pencarian semantik taktik penyerang MITRE ATT&CK dan rekomendasi OWASP Top 10 menggunakan PostgreSQL pgvector.*
  >
  > *Mari kita lihat bagaimana sistem ini bekerja secara langsung dalam lingkungan produksi."*

---

### SCENE 3: LIVE DEMO PENYERANGAN & RESPON OTONOM (01:05 – 02:40)
* **Visual 1 (01:05 - 01:30):**
  - Pindah ke layar **Lab OWASP Juice Shop** di `https://juice.flummox.cloud/`.
  - Buka halaman login atau search bar, lalu masukkan payload SQL Injection nyata:
    ```sql
    ' OR 1=1--
    ```
    atau buka URL search dengan payload:
    `https://juice.flummox.cloud/rest/products/search?q=qwert')) UNION SELECT 1,2,3,4,5,6,7,8,9--`
  - Tekan Enter.
* **Voiceover / Naskah:**
  > *"Di sini kami memiliki lingkungan lab produksi OWASP Juice Shop yang dipantau oleh Nginx reverse proxy dan sistem sensor kami.*
  >
  > *Sekarang, saya akan menyimulasikan seorang peretas yang melancarkan serangan SQL Injection tingkat lanjut untuk membobol basis data pengguna. Saya kirimkan request injeksi ini sekarang..."*

* **Visual 2 (01:30 - 02:15):**
  - Langsung beralih ke tab **SOC Dashboard**: `https://gtnic-hackwitgoh.vercel.app/`.
  - Tunjukkan bahwa dalam **kurang dari 3 detik**, antrean insiden secara otomatis ter-update tanpa me-refresh halaman (fitur real-time auto-polling).
  - Klik baris insiden baru tersebut untuk membuka detail panel investigasi.
* **Voiceover / Naskah:**
  > *"Perhatikan dasbor SOC GTNIC SOAR kami. Tanpa perlu refresh, hanya dalam 3 detik, agen AI kami langsung menangkap serangan, melakukan deduplikasi, dan memicu loop investigasi otonom.*
  >
  > *Perhatikan: agen memanggil fungsi inspect_web_attack, mengekstrak payload, memeriksa riwayat IP di Wazuh, dan memetakan taktik penyerang ke MITRE ATT&CK T1190.*
  >
  > *Hasilnya disintesis ke dalam Attack Story linimasa kronologis, menjelaskan apa yang dicoba dilakukan peretas dan target tabel yang diincar."*

* **Visual 3 (02:15 - 02:40):**
  - Tunjukkan tab notifikasi Discord (jika terpasang), atau perlihatkan bilah statistik di dashboard yang langsung menghitung metrik Active Threats dan Critical Priority.
* **Voiceover / Naskah:**
  > *"Secara bersamaan, agen mengirimkan notifikasi darurat berformat rich embed ke kanal Discord tim keamanan, sehingga insiden berprioritas kritis dapat direspons seketika oleh tim siaga di mana pun mereka berada."*

---

### SCENE 4: BUKTI PRO VS KONTRA, ANTI-HALUSINASI, & HUMAN-IN-THE-LOOP (02:40 – 03:20)
* **Visual:**
  - Scroll ke bagian **Evidence Panel** di dasbor.
  - Sorot kolom **Pro Evidence** (bukti pendukung serangan) dan **Contra Evidence** (bukti meringankan).
  - Sorot bagian **Tool Trace Terminal** yang menampilkan log eksekusi JSON perkakas.
  - Arahkan kursor ke tombol **[Approve Mitigation]** dan klik tombol tersebut. Tunjukkan status berubah menjadi *Approved* dengan rekaman analis dan timestamp.
* **Voiceover / Naskah:**
  > *"Salah satu inovasi terbesar GTNIC SOAR adalah Lapisan Anti-Halusinasi Deterministik.*
  >
  > *Banyak solusi AI membuat halusinasi berbahaya. Di GTNIC SOAR, setiap klaim LLM dicek silang secara matematis terhadap fakta konkret tool. Jika tidak ada bukti mentah, klaim otomatis dieliminasi.*
  >
  > *Lebih jauh lagi, kami menerapkan Bilateral Evidence Matrix—menyajikan bukti yang memberatkan penyerang bersanding dengan bukti yang meringankan, sehingga analis mendapatkan gambaran objektif tanpa bias konfirmasi.*
  >
  > *Dan yang paling penting: kami menganut prinsip Human-in-the-Loop. Agen menyajikan data forensik yang lengkap, tetapi keputusan akhir mitigasi tetap di tangan manusia. Saya klik 'Approve Mitigation', dan sistem mencatat audit trail lengkap untuk kebutuhan regulasi UU PDP."*

---

### SCENE 5: DAMPAK BISNIS, KESIMPULAN & PENUTUP (03:20 – 03:45)
* **Visual:**
  - Tampilkan slide ringkasan metrik dampak:
    - *Waktu Investigasi: 25 Menit → 3–8 Detik (Efisiensi 99,5%)*
    - *Potensi Penghematan IBM: USD 2,2 Juta per Insiden*
    - *Tautan Dashboard & Repo Terbuka*
  - Wajah anggota tim / perwakilan tim menyampaikan penutup.
* **Voiceover / Naskah:**
  > *"Dengan GTNIC SOAR, waktu investigasi insiden dipangkas dari 25 menit menjadi hanya 3 hingga 8 detik—sebuah peningkatan efisiensi lebih dari 99 persen. Berdasarkan riset IBM, implementasi AI SOAR seperti ini berpotensi menghemat kerugian perusahaan hingga 2,2 juta dolar per insiden.*
  >
  > *GTNIC SOAR siap menjadi garda terdepan kedaulatan keamanan digital enterprise Indonesia.*
  >
  > *Terima kasih kepada Dewan Juri GTNIC 2026. Bersama GTNIC SOAR, amankan masa depan digital bangsa!"*

---

## 🛠️ CHECKLIST TEKNIS SEBELUM MEREKAM
1. **Tes URL Juice Shop:** Pastikan `https://juice.flummox.cloud/` bisa diakses lancar.
2. **Tes Dashboard:** Buka `https://gtnic-hackwitgoh.vercel.app/` dan pastikan data insiden termuat.
3. **Payload Serangan Siap Pakai (Tinggal Copy-Paste):**
   - **SQL Injection:** `' UNION SELECT null, email, password, null, null, null, null, null, null FROM Users--`
   - **XSS:** `<iframe src="javascript:alert('GTNIC-SOAR-XSS')">`
   - **Directory Traversal:** `/ftp/legal.md`
4. **Software Rekaman Layar:** Gunakan OBS Studio (disarankan) atau Xbox Game Bar (Win+G) / Loom / Clipchamp.
5. **Editing Ringan:** Pastikan volume suara seimbang dan transisi antarlayar mulus.
