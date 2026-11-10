# PROPOSAL KARYA (UX CASE STUDY)
## GARDA TECH NATIONAL INNOVATION COMPETITION (GTNIC) 2026

**KATEGORI PERLOMBAAN:** AI Agent Development  
**SUB-TEMA:** *"Building Intelligent AI Agents for Enterprise Productivity"*  

---

# GTNIC SOAR
### *Autonomous Multi-Tool AI SOC Agent for Real-Time Threat Investigation, Deterministic Claim Guard, and Auditable Incident Response*

**Disusun Oleh Tim: HackWithGoh**
1. Marcelinus Wijaya Oey — Universitas Bina Nusantara
2. Greshen Chin — Universitas Bina Nusantara
3. Melvin Goh — Universitas Bina Nusantara

**JAKARTA, INDONESIA — 2026**

---

## 1. LATAR BELAKANG MASALAH

### 1.1 Krisis Keamanan Siber di Era Akselerasi Digital Enterprise
Transformasi digital di sektor enterprise, perbankan, telekomunikasi, dan instansi layanan publik Indonesia telah meningkatkan efisiensi operasional secara signifikan. Namun, meningkatnya ketergantungan terhadap infrastruktur digital juga memperbesar risiko gangguan keamanan siber berskala nasional. Salah satu preseden nyata adalah insiden serangan ransomware *Brain Cipher* terhadap Pusat Data Nasional Sementara (PDNS) 2 pada Juni 2024. Insiden tersebut berdampak pada 239 instansi pemerintah dan 282 *tenant* PDNS 2. Pemerintah mengidentifikasi ransomware yang digunakan sebagai pengembangan dari *LockBit 3.0*, dengan pelaku meminta tebusan sebesar USD 8 juta. Insiden ini menunjukkan pentingnya pemantauan keamanan real-time, pencadangan data, serta proses deteksi dan respons insiden yang terkoordinasi dan cepat [8][10].

### 1.2 Eskalasi Ancaman Siber Nasional & Dampak Finansial Global
Berdasarkan data Badan Siber dan Sandi Negara (BSSN) yang diberitakan oleh detikInet (2026), Indonesia mencatat sekitar 5,5 miliar aktivitas serangan siber sepanjang tahun 2025. Jumlah tersebut meningkat lebih dari tujuh kali lipat dibandingkan rata-rata tahunan periode 2020–2024. Kondisi ini menunjukkan tingginya aktivitas ancaman siber di Indonesia dan pentingnya penguatan sistem pemantauan serta deteksi dini terhadap potensi serangan [2]. Laporan Ancaman Digital di Indonesia Semester I 2026 dari AwanPintar.id, sebagaimana diberitakan oleh Kompas.com, mencatat 257.976.333 aktivitas serangan siber selama Januari hingga Juni 2026, atau rata-rata sekitar 16 aktivitas per detik (naik 93,33%). Kategori yang paling dominan adalah *Attempted Administrator Privilege Gain* sebesar 43,65%, yaitu aktivitas percobaan memperoleh hak akses administrator. Temuan ini memperkuat kebutuhan pemantauan dan analisis aktivitas mencurigakan, khususnya upaya eskalasi hak akses sistem [1].

Di tingkat global, *IBM Security (2024)* melaporkan bahwa rata-rata biaya kebocoran data secara global mencapai USD 4,88 juta, meningkat 10% dibandingkan tahun sebelumnya. Sebanyak 70% organisasi yang mengalami kebocoran data menyatakan bahwa insiden tersebut menyebabkan gangguan operasional yang signifikan atau sangat signifikan. Laporan yang sama mencatat bahwa rata-rata siklus kebocoran data mencapai 258 hari. Organisasi yang menggunakan AI dan otomatisasi keamanan secara ekstensif pada alur kerja pencegahan (*prevention workflows*) dapat mengidentifikasi dan menangani insiden rata-rata 98 hari lebih cepat serta berkaitan dengan rata-rata biaya kebocoran data USD 2,2 juta lebih rendah dibandingkan organisasi yang tidak menggunakannya [3].

### 1.3 Hambatan Struktural SOC & Rumusan Solusi Baru
Pusat operasi keamanan (*Security Operations Center* / SOC) enterprise modern menghadapi tiga hambatan struktural:
1. **Defisit Talenta Global**: Kesenjangan tenaga profesional keamanan siber global diperkirakan mencapai 4,8 juta orang berdasarkan studi ISC2 (2024) [4].
2. **Kelelahan Kognitif Analis (*Alert Fatigue*)**: Volume alert keamanan harian yang masif membutuhkan pemantauan berkelanjutan, di mana investigasi manual memakan waktu 20–30 menit per tiket.
3. **Keterbatasan Chatbot Konvensional**: Chatbot AI generatif umumnya berfokus pada dialog teks pasif, rentan berhalusinasi, serta belum memiliki kemampuan untuk mengeksekusi investigasi forensik telemetri secara langsung.

Menjawab krisis ini, kami merumuskan **GTNIC SOAR**: *Autonomous AI SOC Agent Tier-1/Tier-2*. Sistem ini mendengarkan telemetri real-time, mengeksekusi investigasi multi-tahap secara mandiri menggunakan perkakas forensik (*tool calling*), memvalidasi klaim secara deterministik untuk mengeliminasi halusinasi, dan menyajikan matriks bukti berimbang (*Pro vs Contra*) kepada analis dalam kerangka kerja *Human-in-the-Loop*.

---

## 2. TUJUAN, MANFAAT, DAN SOLUSI

### 2.1 Tujuan Pengembangan
1. **Otomasi Investigasi Multi-Tool**: Mengembangkan mesin agen AI otonom menggunakan Gemini 3.8 Flash pada Google Cloud Vertex AI dengan kapabilitas penalaran mandiri dan *multi-tool calling* hingga 3 putaran investigasi berantai.
2. **Eliminasi Halusinasi AI**: Mengimplementasikan lapisan validasi klaim deterministik (*Claim Guard*) berbasis logika terprogram untuk memeriksa kesesuaian klaim AI dengan fakta konkret hasil eksekusi tools, sehingga klaim tanpa bukti pendukung nyata tidak ditampilkan sebagai fakta terkonfirmasi.
3. **Reduksi Drastis MTTD**: Mengembangkan otomasi triase awal dan investigasi digital dengan target waktu pemrosesan 3,5–7 detik per tiket berdasarkan hasil pengujian internal pada 12 skenario lingkungan simulasi.
4. **Tata Kelola Human-in-the-Loop**: Menyediakan antarmuka SOC berbasis web modern yang transparan, menyajikan linimasa serangan (*Attack Story*), taksonomi MITRE ATT&CK [5], matriks bukti *Pro vs Contra*, dan alur persetujuan mitigasi analis.

### 2.2 Manfaat Solusi
- **Bagi Enterprise**: Membantu mempercepat proses triase dan investigasi insiden, mendukung pemantauan keamanan secara berkelanjutan, serta memitigasi potensi kerugian kebocoran data rata-rata USD 2,2 juta (IBM 2024) [3].
- **Bagi Analis SOC**: Mengurangi pekerjaan investigasi yang repetitif melalui otomasi pengumpulan bukti, analisis alert, serta penyajian bukti pendukung (*pro*) dan pembantah (*contra*) sebelum tindakan diambil.
- **Bagi Pimpinan CISO**: Memberikan visibilitas real-time terhadap postur ancaman korporasi melalui *audit trail* forensik lengkap (*auditable AI*) yang akuntabel bagi dewan direksi dan regulator.

### 2.3 Solusi Teknologi yang Ditawarkan
GTNIC SOAR menghadirkan arsitektur agen terintegrasi *end-to-end*: (1) Ingesti telemetri Nginx reverse proxy lab OWASP Juice Shop dan log Wazuh SIEM dengan deduplikasi terarah per IP dan rule ID; (2) Penalaran otonom Gemini 3.8 Flash yang memanggil 4 tools (`search_alerts_by_ip`, `get_login_history`, `inspect_web_attack`, `mitre_owasp_rag`); (3) Verifikasi deterministik Claim Guard terhadap fakta konkret; (4) Matriks bukti bilateral Pro vs Contra; serta (5) Dasbor persetujuan mitigasi oleh analis manusia.

---

## 3. TARGET PENGGUNA / PASAR APLIKASI

### 3.1 Segmen Target
GTNIC SOAR menyasar organisasi yang menghadapi ancaman siber dan kewajiban perlindungan data ketat, namun memiliki keterbatasan jumlah analis keamanan:
- **Segmen Utama**: Sektor *fintech*, *e-commerce*, dan bank digital yang terikat UU PDP No. 27/2022 [7], serta penyedia *Managed Security Service Provider* (MSSP) lokal yang melayani banyak klien.
- **Segmen Sekunder**: Perusahaan skala menengah pengguna Wazuh SIEM, BUMD, rumah sakit, dan perguruan tinggi. Karena dibangun di atas fondasi *open-source* Wazuh, biaya adopsinya terjangkau dengan target awal 8–10 institusi *pilot partner*.

### 3.2 Profil Pengguna (Persona)

| Dimas (24 thn) — Analis Tier-1 | Rian (31 thn) — Incident Responder | Ibu Stephanie (42 thn) — CISO |
| :--- | :--- | :--- |
| **Masalah Utama**: Kelelahan kognitif (*alert fatigue*) menyaring ratusan alert harian; takut melewatkan ancaman nyata. | **Masalah Utama**: Waktu tersita mengumpulkan dan mengorelasikan log secara manual; lambat membuktikan dampak serangan cepat. | **Masalah Utama**: Biaya operasional SOC membengkak; defisit talenta siber; ancaman sanksi UU PDP bila insiden lalai ditangani. |
| **Kebutuhan**: Triase cepat dan pemilahan *false positive* terverifikasi berbasis bukti telemetri konkret. | **Kebutuhan**: Bukti forensik terstruktur (payload, status HTTP, MITRE) tanpa query database manual. | **Kebutuhan**: Visibilitas audit trail lengkap, efisiensi operasional SOC, dan kepatuhan regulasi privasi data. |
| **Solusi SOAR**: Triase otomatis 3,5–7 detik; memilah alert dan menyajikan ringkasan insiden awal. | **Solusi SOAR**: Payload, riwayat IP, dan taktik MITRE tersaji otomatis dalam matriks pro-kontra dan linimasa serangan. | **Solusi SOAR**: Jejak audit lengkap, notifikasi instan Discord, kepatuhan UU PDP (notifikasi 3x24 jam), dan efisiensi biaya. |

### 3.3 Analisis Alur Kerja: Sebelum vs Sesudah

| Tahapan Investigasi | Alur Kerja Manual Konvensional | Alur Kerja GTNIC SOAR | Efisiensi Waktu |
| :--- | :--- | :--- | :---: |
| **1. Pengumpulan Bukti** | Buka Wazuh, cari riwayat IP penyerang (~10 menit) | 4 perkakas forensik otomatis (~3–5 detik) | **99,4%** |
| **2. Analisis Taksonomi** | Cari manual taksonomi MITRE/OWASP di web (~8 menit) | Pencarian vektor pgvector HNSW (~1 detik) | **99,8%** |
| **3. Sintesis & Mitigasi** | Ketik laporan manual & formulasi aksi (~7 menit) | *Attack Story* otomatis & satu klik Approve (~5 detik) | **98,8%** |
| **Total per Tiket Insiden** | **~25–30 Menit** | **3,5–7 Detik** | **> 99%** |

*Catatan: Durasi alur manual merupakan estimasi tim berdasarkan tahapan pekerjaan analis. Durasi GTNIC SOAR diukur secara internal pada 12 skenario uji di lab simulasi.*

---

## 4. FITUR UTAMA & KEUNIKAN APLIKASI

### 4.1 Rincian 12 Fitur Fungsional Utama
- **1. Autonomous Multi-Tool Calling Engine**: Mengimplementasikan siklus ReAct (*Reasoning + Action*) [9] via Gemini 3.8 Flash hingga 3 putaran investigasi berantai mandiri.
- **2. Tool `search_alerts_by_ip`**: Mengagregasi riwayat alert keamanan dari Wazuh Indexer 24 jam terakhir untuk deteksi anomali eskalasi IP penyerang.
- **3. Tool `get_login_history`**: Menganalisis log autentikasi host (rule 100100 login gagal vs 100103 berhasil) untuk deteksi percobaan brute force berdasarkan rasio kegagalan.
- **4. Tool `inspect_web_attack`**: Deep parsing payload web (SQLi & XSS), kode respons server (HTTP 200, 403, 500), serta parameter target (Path Traversal & Cmd Injection dijaga di proxy).
- **5. Tool `mitre_owasp_rag`**: Pencarian kemiripan kosinus (HNSW) pada PostgreSQL pgvector untuk taksonomi MITRE ATT&CK v15 [5] dan mitigasi OWASP Top 10 [6].
- **6. Deterministic Claim Guard**: Verifikasi matematis klaim AI terhadap fakta konkret (`evidence_ref`); status CONFIRMED mewajibkan minimal 2 bukti valid independen tanpa kontradiksi.
- **7. Bilateral Evidence Matrix**: Penyajian fakta berimbang: Bukti Pendukung (*Pro*) bersanding dengan Bukti Meringankan/Kontradiktif (*Contra*) guna mencegah bias konfirmasi.
- **8. Deterministic Scoring Engine**: Skor keparahan (0–100) dan skor keyakinan (0–100%) dihitung formula deterministik berbasis level rule Wazuh dan bukti empiris, bukan opini bebas LLM.
- **9. Real-Time SOC Command Dashboard**: Antarmuka Next.js 15 SOC Dark Theme dengan auto-polling 3 detik (SWR), metrik ringkasan status operasional, dan filter interaktif.
- **10. Human-in-the-Loop Governance**: Tombol tindakan *'Approve Mitigation'* dan *'Reject False Positive'* yang merekam otorisasi analis, stempel waktu ISO 8601, dan riwayat audit utuh.
- **11. Multi-Channel Alerting (Discord & n8n)**: Notifikasi instan berformat rich embed ke kanal Discord operasional via Discord REST API v10 dan webhook n8n secara asinkronus.
- **12. Live Attack Simulation Lab**: Lingkungan simulasi penyerangan berbasis OWASP Juice Shop v17 di balik Nginx proxy untuk demonstrasi dan validasi langsung.

### 4.2 Benchmark Evaluasi Kinerja (GTNIC SOAR vs Baseline)

| Metrik Evaluasi | Analis Manual | Baseline Chatbot Generik | GTNIC SOAR |
| :--- | :---: | :---: | :---: |
| **Waktu Triase per Tiket** | 20 – 30 Menit | 15 – 30 Detik | **3,5 – 6,8 Detik** |
| **Tingkat Halusinasi Klaim** | 0% (Manual) | 28% – 42% (Tinggi) | **0% Klaim Tanpa Bukti (Tervalidasi)** |
| **Korelasi Standar MITRE/OWASP** | Parsial (Manual) | Parsial (Statis) | **100% Otomatis (pgvector RAG)** |
| **Estimasi Kapasitas Triase** | 2 – 3 Tiket / Jam | 10 – 20 Tiket (Pasif) | **400 – 600 Tiket / Jam (Otonom)\*** |
| **Transparansi Jejak Audit** | Alat Manual (Tiket) | 0% (Black Box) | **100% (Tool Trace Terminal)** |
| **Penyajian Bukti Pro vs Kontra** | Jarang (Bias) | Tidak Ada | **Tersedia Lengkap (Bilateral)** |

*\*Catatan: Diuji pada 12 skenario serangan terkalibrasi di lab simulasi OWASP Juice Shop dan dataset telemetri SIEM.*

---

## 5. ARSITEKTUR SISTEM, SKEMA DATABASE & TEKNOLOGI

### 5.1 Stack Teknologi Terpadu

| Komponen Sistem | Teknologi / Perkakas | Versi | Peran & Fungsi Arsitektur |
| :--- | :--- | :---: | :--- |
| **AI Foundation** | Vertex AI Gemini 3.8 Flash | Production | Penalaran agen otonom & tool calling berlatensi rendah. |
| **AI Embedding** | Vertex AI text-embedding-005 | 768-dim | Vektor semantik untuk taksonomi MITRE ATT&CK [5] & OWASP [6]. |
| **Backend Framework** | FastAPI (Python 3.11) | 0.115+ | API asinkronus berkinerja tinggi, Pydantic v2, Swagger docs. |
| **Database Relasional** | PostgreSQL 16 + pgvector | 16.x / 0.7+ | Penyimpanan data transaksi ACID penuh dan indeks HNSW cosine. |
| **Vector Engine** | pgvector Extension | 0.7+ | Pencarian kemiripan kosinus sub-milidetik taksonomi MITRE. |
| **SIEM Platform** | Wazuh Manager & Indexer | 4.9.0 / 4.8+ | Agregasi log host & alert jaringan berbasis OpenSearch. |
| **Lab Target** | OWASP Juice Shop | 17.x | Lingkungan web rentan standar industri untuk simulasi serangan. |
| **Reverse Proxy** | Nginx HTTP Proxy | 1.27-alpine | Penyaring lalu lintas HTTP & penangkap log JSON (*juice_json*). |
| **Frontend Framework** | Next.js (React 19) + TypeScript | 15.x | Server-Side Rendering, App Router modern, deploy di Vercel. |
| **Styling System** | Tailwind CSS + Lucide Icons | 3.4+ | Antarmuka Cyberpunk High-Tech SOC Dark Theme ergonomis. |
| **Data Polling Layer** | SWR (*Stale-While-Revalidate*) | 2.2+ | Auto-polling adaptif 3 detik tanpa refresh halaman. |
| **Notifikasi Cepat** | Discord REST API v10 + n8n | Current | Kirim notifikasi rich embed darurat asinkronus ke kanal tim. |

### 5.2 Alur Arsitektur Sistem Modular (End-to-End Flow)
Sistem dibangun dengan arsitektur berlapis yang memisahkan persepsi, penalaran, validasi, dan presentasi:
1. **Lapisan Persepsi**: Nginx reverse proxy menangkap log HTTP JSON lab Juice Shop dan Wazuh SIEM mengumpulkan log host.
2. **Lapisan Deduplikasi & Ingesti**: Backend FastAPI mengelompokkan alert per IP dan rule ID dalam jendela waktu 60 detik.
3. **Lapisan Penalaran Otonom**: Model Gemini 3.8 Flash mengevaluasi alert dan memanggil 4 tools forensik mandiri dalam siklus ReAct [9].
4. **Lapisan Penjamin Kebenaran**: Claim Guard menguji silang klaim terhadap fakta konkret (`evidence_ref`) dan menghitung skor deterministik.
5. **Lapisan Presentasi**: Dasbor Next.js 15 menampilkan Attack Story, bukti Pro vs Contra, dan gerbang otorisasi Approve Mitigation.

### 5.3 Formulasi Matematis: Anti-Halusinasi & Skoring Deterministik
1. **Validitas Bukti & Aturan Status**:
   - Setiap bukti $e$ wajib memiliki rujukan persis ke himpunan fakta empiris hasil alat ($\text{evidence\_ref} \in F_{\text{empiris}}$).
   - Bukti pro efektif ($E_{\text{pro\_eff}}$) dibatasi maksimal 2 per tool.
   - Status **CONFIRMED** mewajibkan $|E_{\text{pro\_eff}}| \ge 2$, berasal dari minimal 2 tool independen berbeda, dan $|E_{\text{contra}}| = 0$.
   - Jika bukti pro valid $\ge 1$ namun belum memenuhi syarat mutlak, status ditetapkan **LIKELY**. Jika bukti valid nihil atau data inkonsisten, status otomatis **UNCERTAIN**.
2. **Skor Keparahan Deterministik ($S$)**:
   $$S = \text{clamp}\Big(10, 100, (L_{\text{wazuh}} \times 5) + (\min(|E_{\text{pro\_eff}}|, 4) \times 10) - (\min(|E_{\text{contra}}|, 4) \times 12) + \Delta_{\text{confirmed}}\Big)$$
   *Di mana $L_{\text{wazuh}}$ adalah level rule Wazuh (1–15), kontribusi bukti pro efektif maksimal +40 poin, penalti kontra maksimal -48 poin, dan bonus $\Delta_{\text{confirmed}} = +20$ khusus jika status CONFIRMED. Klasifikasi: Critical ($S \ge 80$), High ($60 \le S < 80$), Medium ($40 \le S < 60$), dan Low ($S < 40$).*
3. **Skor Keyakinan Deterministik ($C$)**:
   $$C = \text{clamp}\Big(0, 100, \text{round}\big(100 \times (0.5 \times \text{Validity} + 0.5 \times \text{Coverage})\big) - P_{\text{inconsistent}} - P_{\text{claim}}\Big)$$
   *Di mana $\text{Validity} = |E_{\text{valid}}| / |E_{\text{claimed}}|$, $\text{Coverage} = \min(1.0, |\text{Tools}| / 3)$, $P_{\text{inconsistent}} = 20$ penalti anomali telemetri, dan $P_{\text{claim}} = 10$ penalti per klaim tanpa bukti.*

### 5.4 Skema Basis Data Relasional & Vektor

| Nama Tabel | Tipe & Mesin Basis Data | Peran & Atribut Kunci |
| :--- | :--- | :--- |
| `incidents` | Relasional (PostgreSQL 16) | Menyimpan 27 atribut entitas insiden: *raw_alert*, *status*, *severity*, *confidence*, *attack_story*, *pro/contra evidence*, *tool_trace*, *decided_by*, *latency*. |
| `security_knowledge` | Vector DB (pgvector HNSW) | Menyimpan konten taksonomi MITRE ATT&CK [5] & OWASP Top 10 [6] beserta vektor embedding 768-dim dengan cosine distance ops. |
| `alert_dedup` | Relasional In-Memory/Disk | Tabel pelacakan deduplikasi alert per alamat IP sumber dan rule ID untuk memitigasi badai alert redundan. |
| `benchmark_runs` | Relasional Evaluasi | Mencatat metrik komparasi 12 skenario pengujian: expected vs agent verdict, evidence validity ratio, token count, dan latensi (ms). |

---

## 6. BATASAN SISTEM APLIKASI
- **1. Pertahanan Pasif & Human Approval Gate**: Agen secara sengaja dikonfigurasi dalam mode read-only mitigasi. Tombol *'Approve Mitigation'* mencatat otorisasi analis manusia dan merekam audit trail forensik ke database, bukan langsung memodifikasi firewall secara sepihak (otomasi firewall aktif dijadwalkan pada Roadmap Fase 1).
- **2. Ruang Lingkup Deteksi**: Sensor web terfokus pada spektrum OWASP Top 10 utama [6] (SQLi dan XSS pada perkakas investigasi agen, serta Path Traversal dan Command Injection pada ingress gateway proxy).
- **3. Fail-Safe Local Triage**: Jika koneksi ke Vertex AI terputus atau batas kuota tercapai, sistem secara otomatis beralih ke *Local Triage Heuristic Engine* sehingga fungsi pemantauan dasar dan pencatatan insiden tidak terhenti.
- **4. Arsitektur Multi-Tenant**: Dasbor saat ini dioptimalkan untuk satu entitas enterprise (*single-tenant*) dan belum mendukung partisi data multi-organisasi untuk penyedia MSSP besar.

---

## 7. TANGKAPAN LAYAR (SCREENSHOT) ANTARMUKA
*[Sisipkan screenshot dari halaman-halaman utama sistem yang telah Anda deploy (responsif). Berikan sedikit caption/penjelasan fungsi pada tiap screenshot.]*

- **[ TEMPAT PENEMPATAN SCREENSHOT: Gambar 1: Antarmuka Real-Time Incident Feed & Metrik Status Operasional SOC (Live Next.js 15 Dark Theme) ]**
- **[ TEMPAT PENEMPATAN SCREENSHOT: Gambar 2: Detail Rekonstruksi Serangan (Attack Story Timeline) & Matriks Bukti Bilateral Pro vs Contra ]**
- **[ TEMPAT PENEMPATAN SCREENSHOT: Gambar 3: Transparansi Tool Trace Terminal, Skor Deterministik, dan Rekomendasi Mitigasi Analis ]**
- **[ TEMPAT PENEMPATAN SCREENSHOT: Gambar 4: Integrasi Notifikasi Insiden Real-Time Rich Embed pada Kanal Discord Tim SOC ]**

---

## 8. RENCANA PENGEMBANGAN LANJUTAN (FUTURE DEVELOPMENT)
Peta jalan pengembangan strategis GTNIC SOAR untuk implementasi skala industri terbagi ke dalam 5 fase terukur:

| Fase & Target Waktu | Target Inovasi | Deskripsi & Dampak Operasional Industri |
| :--- | :--- | :--- |
| **Fase 1: Q1 2027** | Active Response Firewall Automation | Integrasi aksi *Approve Mitigation* langsung ke Cloudflare WAF, AWS Security Group, dan Wazuh Active Response untuk isolasi IP otomatis <1s. |
| **Fase 2: Q2 2027** | Threat Intelligence Feeds Enrichment | Integrasi perkakas agen ke API VirusTotal, AbuseIPDB, Shodan, dan AlienVault OTX untuk verifikasi reputasi ancaman global. |
| **Fase 3: Q3 2027** | Automated Compliance PDF Report | Modul generator laporan kepatuhan regulasi UU PDP Pasal 46 [7] dan ISO 27001 format PDF resmi bertanda tangan digital untuk audit CISO. |
| **Fase 4: Q4 2027** | Multi-Tenant MSSP & Enterprise RBAC | Arsitektur multi-penyewa dengan kontrol akses berbasis peran (Tier-1, Tier-2, Manager) untuk melayani banyak klien enterprise. |
| **Fase 5: 2028** | Adaptive Autonomous Honeypot Deception | Kapabilitas agen mengalihkan peretas tingkat tinggi (APT) ke sistem umpan tiruan guna mempelajari taktik baru tanpa membahayakan data inti. |

---

## 9. TAUTAN PENTING (LAMPIRAN)
Sebagai bahan verifikasi dan evaluasi menyeluruh Dewan Juri GTNIC 2026, berikut adalah tautan proyek kami:
- **Tautan Sistem / Prototype Live**: [https://gtnic-hackwitgoh.vercel.app/](https://gtnic-hackwitgoh.vercel.app/) *(Aktif 24/7 di jaringan Vercel Edge dan dapat diuji langsung oleh Dewan Juri).*
- **Tautan Lingkungan Lab Serangan (OWASP Juice Shop)**: [https://juice.flummox.cloud/](https://juice.flummox.cloud/) *(Lab aplikasi web target yang terintegrasi langsung dengan sensor reverse proxy).*
- **Tautan Repositori / Dokumentasi Lengkap**: [https://github.com/Greshen-Chin/GTNIC_AI_AGENT](https://github.com/Greshen-Chin/GTNIC_AI_AGENT) *(Kode sumber backend FastAPI, frontend Next.js, aturan Wazuh, dan dokumentasi arsitektur).*
- **Tautan Video Demo YouTube**: `[Tautan Video Demo YouTube (Mode Publik atau Unlisted)]` *(Demonstrasi end-to-end simulasi serangan hingga mitigasi otomatis).*

---

## DAFTAR PUSTAKA

1. AwanPintar.id. (2026). *Laporan Ancaman Digital di Indonesia Semester I 2026: Dalam Sedetik, 16 Serangan Siber Hantam Indonesia*. Kompas.com & PT Media Antar Nusa. `[Dikutip di Bab 1.2]`
2. Haryanto, A. T. (2026, 23 April). *Duh, RI Dihantam 1,5 Miliar Anomali Trafik dalam 4 Bulan*. detikInet & Badan Siber dan Sandi Negara (BSSN). `[Dikutip di Bab 1.2]`
3. IBM Security. (2024). *Cost of a Data Breach Report 2024: Escalating Data Breach Disruption Pushes Costs to New Highs*. Ponemon Institute & IBM Security Services. `[Dikutip di Bab 1.2, 2.2]`
4. ISC2. (2024). *2024 ISC2 Cybersecurity Workforce Study: Addressing the Global Talent Shortage*. Clearwater, FL: ISC2. `[Dikutip di Bab 1.3]`
5. MITRE Corporation. (2024). *Updates - April 2024: MITRE ATT&CK Framework Enterprise Matrix v15*. Bedford, MA: The MITRE Corporation. `[Dikutip di Bab 2.1, 4.1, 5.1]`
6. OWASP Foundation. (2025). *OWASP Top 10:2025 - The Ten Most Critical Web Application Security Risks*. OWASP Foundation. `[Dikutip di Bab 4.1, 5.1, 6]`
7. Republik Indonesia. (2022). *Undang-Undang RI Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)*. Lembaran Negara RI Tahun 2022 No. 196. `[Dikutip di Bab 3.1, 8]`
8. Badan Siber dan Sandi Negara (BSSN). (2024). *Laporan Forensik Insiden Siber Pusat Data Nasional Sementara (PDNS) 2: Identifikasi Serangan Ransomware Brain Cipher*. Jakarta: BSSN RI. `[Dikutip di Bab 1.1]`
9. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. International Conference on Learning Representations (ICLR 2023). `[Dikutip di Bab 4.1, 5.2]`
10. Kementerian Komunikasi dan Informatika (Kominfo), BSSN, & PT Telkom Indonesia. (2024). *Siaran Pers Bersama: Penanganan dan Percepatan Pemulihan Layanan Publik Pasca-Gangguan PDNS 2*. Jakarta: Kemkominfo. `[Dikutip di Bab 1.1]`

*(Catatan Pengurangan: Entri SANS 2024 SOC Survey telah dihapus secara resmi dari Daftar Pustaka karena tidak memiliki rujukan sitasi aktif di dalam badan teks).*

