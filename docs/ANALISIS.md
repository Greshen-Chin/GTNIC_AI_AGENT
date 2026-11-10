# 📋 Analisis Proposal GTNIC SOAR — Pemetaan Lengkap untuk Lomba GTNIC 2026

**Dokumen internal tim — Panduan pengisian proposal berdasarkan Guide Book, Template, dan Codebase**

---

## 1. IDENTITAS KEIKUTSERTAAN

| Item | Isian |
|---|---|
| **Nama Kompetisi** | Garda Tech National Innovation Competition (GTNIC) 2026 |
| **Kategori** | **AI Agent Development** |
| **Sub-Tema** | **"Building Intelligent AI Agents for Enterprise Productivity"** |
| **Fokus Industri** | **Enterprise & Industry** |
| **Tantangan Resmi** | *"Bagaimana AI Agent dapat membantu perusahaan dalam mengotomatisasi pekerjaan, menganalisis data, dan meningkatkan efisiensi operasional?"* |
| **Nama Produk / Agent** | **GTNIC SOAR** — Autonomous AI SOC Agent for Enterprise Cybersecurity Operations |
| **Format Nama File** | `GTNIC2026_AIAgent_[NamaTim].pdf` |

---

## 2. MENGAPA CYBERSECURITY SOC MASUK SUB-TEMA INI?

### 2.1 Kecocokan dengan Sub-Tema

Guide Book menyebutkan contoh projek: *AI Customer Service Assistant, AI Sales Assistant, AI Recruitment Agent, AI Finance Assistant, AI Data Analyst Agent, AI Document Processing Agent*.

Cybersecurity SOC Agent **tidak disebutkan eksplisit**, namun **sepenuhnya masuk cakupan** sub-tema karena:

> [!IMPORTANT]
> Sub-tema berbunyi: **"Building Intelligent AI Agents for Enterprise Productivity"** dengan fokus **Enterprise & Industry**. Tantangannya: **mengotomatisasi pekerjaan, menganalisis data, dan meningkatkan efisiensi operasional**.

| Kriteria Sub-Tema | Bagaimana GTNIC SOAR Memenuhinya |
|---|---|
| *Enterprise* | SOC (Security Operations Center) adalah **divisi wajib** di setiap perusahaan enterprise (bank, telekomunikasi, e-commerce, BUMN). Bukan proyek mainan. |
| *Mengotomatisasi pekerjaan* | Agent **mengotomatisasi investigasi alert** keamanan yang sebelumnya dilakukan manual oleh analis SOC Tier-1 selama ~25 menit per insiden. |
| *Menganalisis data* | Agent **menganalisis log Wazuh SIEM**, melakukan **RAG retrieval** dari knowledge base MITRE ATT&CK + OWASP, dan menghitung **severity + confidence score** secara deterministik. |
| *Meningkatkan efisiensi operasional* | Waktu investigasi turun dari **~25 menit → 3-8 detik** (penghematan **99.5%**). Analis SOC bisa fokus pada insiden yang benar-benar memerlukan keahlian manusia. |

### 2.2 Contoh projek Guide Book yang paling mirip

**GTNIC SOAR paling dekat dengan "AI Data Analyst Agent"** — tetapi di domain keamanan siber enterprise. Agent ini:
- Menganalisis data alert keamanan (bukan data penjualan/keuangan, tapi data ancaman siber)
- Membuat laporan investigasi terstruktur dengan bukti pro vs kontra
- Menyediakan rekomendasi tindakan mitigasi bagi pengambil keputusan (analis SOC)

> Daftar contoh Guide Book bersifat **ilustratif, bukan eksklusif**. Panitia menulisnya sebagai inspirasi. Selama produk menjawab tantangan "membantu perusahaan mengotomatisasi dan menganalisis data untuk efisiensi operasional", sub-tema terpenuhi.

---

## 3. LATAR BELAKANG MASALAH — DATA DAN FAKTA TERKINI

### 3.1 🇮🇩 Krisis Keamanan Siber Indonesia: Data Terbaru

#### Serangan PDN (Pusat Data Nasional) — Juni 2024
- **20 Juni 2024**: Ransomware **Brain Cipher** (varian LockBit 3.0) menyerang **PDNS 2 Surabaya**
- **282 layanan publik** di lebih dari **200 instansi pemerintah** lumpuh total
- **Sistem imigrasi bandara internasional** (termasuk Soekarno-Hatta) down — antrean panjang, pemeriksaan paspor harus dilakukan manual
- Peretas menuntut tebusan **USD 8 juta (Rp 131 miliar)** — pemerintah menolak membayar
- **Hanya 30% server** yang memiliki backup data memadai — sisanya tidak bisa dipulihkan
- Deteksi butuh waktu **hingga 8 jam** karena tidak ada monitoring 24/7 real-time

> **Kunci untuk proposal**: Insiden PDN membuktikan bahwa Indonesia **sangat membutuhkan** sistem pemantauan dan investigasi keamanan siber yang otonom, real-time, dan transparan. Inilah yang GTNIC SOAR sediakan.

#### Volume Serangan Siber Indonesia (Data BSSN)

| Periode | Volume Serangan/Anomali | Sumber |
|---|---|---|
| **2024** | Indonesia masuk **Top 5 negara** paling sering diserang secara global | BSSN |
| **2025** | **5,5 miliar** anomali/serangan siber (naik **714%** dari rata-rata 2020–2024) | BSSN |
| **Jan–Jul 2025** | **3,64 miliar** anomali; 93,78% berkaitan dengan potensi malware → ransomware | BSSN |
| **Jan–Apr 2026** | **1,52 miliar** serangan dalam 3,5 bulan pertama | BSSN |
| **Semester I 2026** | **257,98 juta** serangan terukur (naik **93,33%** dari semester I 2025) | AwanPintar.id |

#### Tren Serangan 2024–2026
- **Privilege Escalation** melonjak: peretas kini mengincar **kendali penuh sistem**, bukan sekadar defacement
- **Sektor paling rentan**: Keuangan/Perbankan, Lembaga Pemerintahan, Layanan Publik
- **Ancaman baru**: AI-driven cyber threats, IoT vulnerabilities, supply chain compromise

### 3.2 🌍 Data Global: Biaya dan Dampak Pelanggaran Keamanan

#### IBM Cost of a Data Breach Report 2024

| Metrik | Angka | Implikasi |
|---|---|---|
| **Rata-rata kerugian per insiden** | **USD 4,88 juta** (naik 10% YoY) | Setiap insiden yang terlambat ditangani = kerugian miliaran rupiah |
| **Waktu identifikasi (MTTD)** | **194 hari** | Tanpa AI agent, rata-rata perusahaan butuh >6 bulan untuk menyadari mereka diserang |
| **Waktu penanggulangan (MTTR)** | **64 hari** | Setelah tahu diserang, masih butuh 2 bulan untuk mengatasi |
| **Total siklus insiden** | **258 hari** | 8,5 bulan dari serangan sampai selesai ditangani |
| **Penghematan dengan AI+Automasi** | **USD 2,2 juta** per insiden | Perusahaan yang deploy AI/automasi di SOC **menghemat Rp35 miliar per insiden** |

#### Alert Fatigue & Kekurangan Tenaga

| Fakta | Angka | Sumber |
|---|---|---|
| Alert yang tidak diinvestigasi | **>50%** alert keamanan dibiarkan karena kelelahan | Riset industri |
| Burnout analis SOC | **71%** analis SOC mengalami burnout profesional | ISC2 / Industry |
| Kekurangan tenaga siber global | **4,8 juta** posisi tidak terisi (naik 19% YoY) | ISC2 2024 |
| False positive memakan waktu | **~33%** waktu investigasi habis untuk alert palsu | Riset industri |

### 3.3 Kesimpulan untuk Proposal

> Kombinasi **5,5 miliar serangan di Indonesia (2025)**, insiden PDN yang melumpuhkan **282 layanan publik**, kekurangan **4,8 juta tenaga siber global**, dan **71% analis SOC burnout** menciptakan **kebutuhan mendesak** akan AI Agent yang mampu menginvestigasi ancaman secara otonom, transparan, dan akuntabel — bukan sekadar chatbot yang menjawab pertanyaan.
>
> **GTNIC SOAR hadir untuk menjawab kebutuhan ini.**

---

## 4. PEMETAAN ISI PROPOSAL (Template → Kode)

### Bagian 1: Latar Belakang Masalah ✍️
**Isi dari**: Data di Bagian 3 di atas + konteks PDN + statistik IBM/BSSN

Narasi yang direkomendasikan:
1. Mulai dari insiden PDN Juni 2024 yang melumpuhkan imigrasi Indonesia → bukti nyata ancaman siber enterprise
2. Hubungkan ke data BSSN: 5,5 miliar serangan di 2025, naik 714%
3. Masalah: analis SOC kewalahan (alert fatigue, 71% burnout, 4,8 juta posisi kosong)
4. Tanpa AI, investigasi satu insiden butuh ~25 menit → ribuan alert per hari = mustahil ditangani manual
5. Solusi yang dibutuhkan: AI Agent otonom yang bukan sekadar chatbot, tapi benar-benar menjalankan investigasi, memvalidasi bukti, dan menyajikan rekomendasi ke manusia

---

### Bagian 2: Tujuan, Manfaat, dan Solusi ✍️

**2.1 Tujuan:**
1. Membangun AI Agent otonom yang mampu menginvestigasi alert keamanan siber secara mandiri menggunakan Gemini tool calling pada Google Cloud Vertex AI
2. Menyediakan dashboard SOC real-time dengan bukti terverifikasi (pro vs kontra) untuk mendukung pengambilan keputusan analis
3. Mengintegrasikan pipeline end-to-end: SIEM (Wazuh) → AI Agent → Dashboard → Notifikasi (Discord/n8n)

**2.2 Manfaat:**
- ⏱️ **Penghematan waktu**: Investigasi insiden dari ~25 menit → **3–8 detik** (penghematan 99,5%)
- 💰 **Penghematan biaya**: Menurut IBM, organisasi dengan AI+automasi hemat **USD 2,2 juta** per insiden
- 🧠 **Mengurangi alert fatigue**: Validasi deterministik + confidence scoring memisahkan true positive dari false positive
- 📋 **Audit trail lengkap**: Setiap keputusan AI bisa ditelusuri kembali ke data faktual dari tool
- 👤 **Human-in-the-Loop**: Manusia tetap pengambil keputusan akhir; AI menyajikan bukti, bukan memutuskan sendiri

**2.3 Solusi:**
- **GTNIC SOAR**: Autonomous AI SOC Agent yang menjalankan tool calling loop (hingga 3 putaran), mengumpulkan bukti dari Wazuh Indexer dan knowledge base MITRE ATT&CK / OWASP Top 10 via RAG, kemudian menghasilkan investigasi terstruktur dengan **validasi anti-halusinasi deterministik**

---

### Bagian 3: Target Pengguna ✍️

| Persona | Deskripsi | Kebutuhan |
|---|---|---|
| **SOC Analyst Tier-1** | Analis junior yang menangani ribuan alert per hari | Butuh triase otomatis agar fokus pada ancaman nyata |
| **SOC Analyst Tier-2** | Analis senior yang menginvestigasi insiden eskalasi | Butuh bukti terstruktur (pro vs kontra) untuk keputusan cepat |
| **CISO / Security Manager** | Pengambil keputusan strategis keamanan perusahaan | Butuh visibilitas real-time atas postur keamanan dan akuntabilitas AI |
| **MSSP (Managed Security Service Provider)** | Perusahaan penyedia jasa keamanan | Butuh platform multi-klien untuk monitoring efisien |
| **Institusi Pendidikan Cybersecurity** | Kampus/pelatihan yang mengajar keamanan siber | Butuh lab interaktif (Juice Shop) + dashboard untuk demonstrasi |

---

### Bagian 4: Fitur Utama & Keunikan ✍️

**4.1 Fitur Utama (12 fitur yang sudah dibangun):**

| # | Fitur | Deskripsi | File Kode |
|---|---|---|---|
| 1 | **Autonomous Tool Calling Loop** | Agent memanggil 4 tool investigasi secara mandiri via Vertex AI Gemini (hingga 3 putaran) | `agent_service.py` |
| 2 | **Tool 1: search_alerts_by_ip** | Query Wazuh Indexer untuk alert terkait dari IP sumber dalam 24 jam terakhir | `wazuh_service.py` |
| 3 | **Tool 2: get_login_history** | Agregasi riwayat login gagal vs berhasil per IP | `wazuh_service.py` |
| 4 | **Tool 3: inspect_web_attack** | Deep inspection payload SQLi & XSS: klasifikasi, HTTP status, parameter target | `wazuh_service.py` |
| 5 | **Tool 4: mitre_owasp_rag** | RAG retrieval dari knowledge base MITRE ATT&CK + OWASP Top 10 menggunakan embedding Vertex AI + pgvector | `rag_service.py` |
| 6 | **Anti-Halusinasi (Deterministic Validator)** | Setiap klaim LLM di-cross-check terhadap fakta konkret dari tool; klaim tanpa bukti otomatis dihapus | `validate_and_score()` |
| 7 | **Pro vs Contra Evidence** | Bukti yang mendukung DAN melemahkan dugaan serangan disajikan bersebelahan | Schema `pro_evidence`, `contra_evidence` |
| 8 | **Deterministic Severity & Confidence Scoring** | Skor keparahan dan keyakinan dihitung dengan formula deterministik, bukan opini LLM | `validate_and_score()` |
| 9 | **Real-time SOC Dashboard** | Polling 3 detik, filter severity/verdict, search, detail insiden dengan 3-column layout | Next.js 15 frontend |
| 10 | **Human-in-the-Loop Decision** | Tombol Approve Mitigation / Reject False Positive dengan audit trail (`decided_by`, `decided_at`) | `dashboard.py` |
| 11 | **Discord Bot Notification** | Embed kaya dengan severity, payload, attack summary dikirim real-time ke channel tim | `discord_service.py` |
| 12 | **Juice Shop Attack Lab** | Monitoring live terhadap OWASP Juice Shop via Nginx reverse proxy + log forwarder; deteksi SQLi, XSS, Path Traversal, Command Injection | `ingest.py`, `middleware.py` |

**4.2 Keunikan vs Solusi yang Ada:**

| Aspek | ChatGPT Wrapper / Chatbot Biasa | GTNIC SOAR |
|---|---|---|
| Arsitektur | Satu prompt → satu jawaban teks | **Tool calling loop multi-putaran** dengan 4 tool berbeda |
| Sumber data | Pengetahuan umum LLM | **Data faktual real-time** dari Wazuh SIEM + RAG pgvector |
| Validasi output | Tidak ada; LLM bisa halusinasi | **Validator deterministik**: setiap bukti dicek terhadap fakta tool |
| Transparansi | Black box | **Full audit trail**: input/output setiap tool terekam |
| Bukti keputusan | Tidak terstruktur | **Pro vs Contra Evidence** — dua sisi argumentasi |
| Peran manusia | Tidak ada | **Human-in-the-Loop**: AI menyajikan, manusia memutuskan |
| Deployment | Chatbox/Streamlit sederhana | **Enterprise-grade SOC Dashboard** + Docker + CI/CD |

---

### Bagian 5: Arsitektur Sistem ✍️

**5.1 Tech Stack:**

| Layer | Teknologi |
|---|---|
| LLM / AI | Google Cloud Vertex AI — Gemini 3.8 Flash (Tool Calling, temperature=0.0) |
| Embedding | Vertex AI `text-embedding-004` (768 dimensi) |
| Backend Framework | Python 3.11, FastAPI 0.162, Uvicorn |
| Database | PostgreSQL 16 + pgvector (HNSW cosine index) |
| SIEM | Wazuh Manager + Wazuh Indexer (OpenSearch) |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, SWR (auto-polling 3s) |
| Notifikasi | Discord Bot (REST API v10), n8n webhook |
| Orchestration | Docker Compose (6 containers: PostgreSQL, soar-api, Juice Shop, Nginx proxy, log forwarder, n8n) |
| Target Lab | OWASP Juice Shop |
| CI/CD | GitHub Actions (self-hosted runner pada GCP VM) |
| Hosting | Google Compute Engine (backend), Vercel (frontend) |
| Autentikasi | Token-based: `X-Internal-Token` (agent/n8n) + `X-Dashboard-API-Key` (dashboard) |

**5.2 Alur Sistem (System Architecture):**

```
                    ┌──────────────────────────────────────────────┐
                    │              SUMBER DATA                     │
                    │                                              │
                    │  ┌─────────────┐    ┌────────────────────┐   │
                    │  │ Wazuh SIEM  │    │ OWASP Juice Shop   │   │
                    │  │ (Alerts DB) │    │ (via Nginx Proxy)  │   │
                    │  └──────┬──────┘    └─────────┬──────────┘   │
                    └─────────┼─────────────────────┼──────────────┘
                              │                     │
                    ┌─────────▼─────────────────────▼──────────────┐
                    │         GTNIC SOAR BACKEND (FastAPI)         │
                    │                                              │
                    │  ┌────────────────────────────────────────┐  │
                    │  │    🤖 AUTONOMOUS AI AGENT ENGINE       │  │
                    │  │                                        │  │
                    │  │  ┌──────────┐    ┌──────────────────┐  │  │
                    │  │  │ Vertex   │◄──►│ Tool Calling     │  │  │
                    │  │  │ AI       │    │ Loop (max 3      │  │  │
                    │  │  │ Gemini   │    │ rounds)          │  │  │
                    │  │  └──────────┘    └────────┬─────────┘  │  │
                    │  │                           │            │  │
                    │  │  ┌──────────────────┐     │            │  │
                    │  │  │ 4 Tools:         │◄────┘            │  │
                    │  │  │ • search_alerts  │                  │  │
                    │  │  │ • login_history  │                  │  │
                    │  │  │ • inspect_web    │                  │  │
                    │  │  │ • mitre_rag      │                  │  │
                    │  │  └──────────────────┘                  │  │
                    │  │                                        │  │
                    │  │  ┌──────────────────────────────────┐  │  │
                    │  │  │ 🛡️ ANTI-HALUSINASI LAYER        │  │  │
                    │  │  │ • Deterministic Validator        │  │  │
                    │  │  │ • Claim Guard                    │  │  │
                    │  │  │ • Severity & Confidence Scorer   │  │  │
                    │  │  │ • Pro vs Contra Evidence Split   │  │  │
                    │  │  └──────────────────────────────────┘  │  │
                    │  └────────────────────────────────────────┘  │
                    │                                              │
                    │  ┌────────────┐  ┌──────────┐  ┌─────────┐  │
                    │  │ PostgreSQL │  │ Auth     │  │ Discord │  │
                    │  │ + pgvector │  │ Layer    │  │ + n8n   │  │
                    │  │ (RAG KB)   │  │ (Token)  │  │ Webhook │  │
                    │  └────────────┘  └──────────┘  └─────────┘  │
                    └──────────────────┬───────────────────────────┘
                                       │ REST API (/api/*)
                                       ▼
                    ┌──────────────────────────────────────────────┐
                    │       SOC DASHBOARD (Next.js 15 / Vercel)   │
                    │                                              │
                    │  ┌──────────┐ ┌────────┐ ┌───────────────┐  │
                    │  │ Incident │ │Evidence│ │ Attack Story  │  │
                    │  │ Queue +  │ │Pro vs  │ │ Timeline      │  │
                    │  │ Stats    │ │Contra  │ │               │  │
                    │  └──────────┘ └────────┘ └───────────────┘  │
                    │  ┌──────────┐ ┌────────────────────────┐    │
                    │  │ MITRE +  │ │ Tool Trace Terminal    │    │
                    │  │ OWASP    │ │ (Audit Log)            │    │
                    │  └──────────┘ └────────────────────────┘    │
                    │                                              │
                    │  ┌────────────────────────────────────────┐  │
                    │  │  👤 HUMAN-IN-THE-LOOP                 │  │
                    │  │  [✅ Approve Mitigation]               │  │
                    │  │  [❌ Reject / False Positive]          │  │
                    │  └────────────────────────────────────────┘  │
                    └──────────────────────────────────────────────┘
```

**5.3 Database Schema:**

| Tabel | Kolom Utama | Fungsi |
|---|---|---|
| **`incidents`** | id, title, source_ip, raw_alert, status, severity_score, confidence_score, attack_story, pro_evidence, contra_evidence, invalid_evidence, tool_trace, mitre_context, human_decision, decided_by, decided_at, llm_model, latency_ms (27 kolom) | Menyimpan insiden investigasi lengkap |
| **`security_knowledge`** | id, source, content, metadata, embedding VECTOR(768) | Knowledge base RAG untuk MITRE ATT&CK + OWASP Top 10 |
| **`alert_dedup`** | key, window_start, hits | Deduplikasi alert 60 detik per srcip+rule_id |
| **`benchmark_runs`** | scenario_name, expected_verdict, agent_verdict, baseline_verdict, evidence_valid_ratio | Evaluasi performa Agent vs Baseline |

---

### Bagian 6: Batasan Sistem ✍️

1. **Agent bersifat read-only** — tidak memblokir IP atau memodifikasi firewall secara otomatis (by design: mencegah agent melakukan tindakan destruktif tanpa persetujuan manusia)
2. Deteksi serangan Juice Shop menggunakan **regex pattern matching** (heuristic), bukan deep packet inspection
3. Bergantung pada koneksi **Google Cloud Vertex AI** untuk mode LLM penuh; tanpa koneksi, fallback ke local triage deterministik yang tetap fungsional
4. Confidence score pada jalur deteksi pola Juice Shop bersifat **fixed 80%**, bukan hasil penilaian per-request
5. Belum ada fitur **export PDF** laporan eksekutif untuk CISO/auditor
6. Dashboard belum mendukung **multi-tenant** (satu organisasi per deployment)

---

### Bagian 7: Screenshot ✍️

Ambil dari dashboard live: `https://gtnic-hackwitgoh.vercel.app/`

Screenshot yang direkomendasikan:
1. **Incident Queue & Threat Triage** — halaman utama dengan stats bar dan tabel insiden
2. **Stats Bar** — Active Threat Queue, Critical Priority, Enforced Mitigations, Avg Confidence
3. **Detail Insiden — Header** — judul, severity badge, verdict badge, source IP, confidence score
4. **Attack Story Timeline** — kronologi langkah serangan yang diidentifikasi AI
5. **Pro vs Contra Evidence Panel** — bukti bersebelahan (inculpatory vs exculpatory)
6. **MITRE ATT&CK & OWASP Panel** — referensi framework keamanan terkait insiden
7. **Tool Trace Terminal** — audit log setiap pemanggilan tool (input, output, durasi)
8. **Tombol Approve/Reject** — mekanisme Human-in-the-Loop
9. **Discord Bot Notification** — embed notifikasi insiden di channel Discord (jika ada screenshot)

---

### Bagian 8: Rencana Pengembangan ✍️

| Fitur | Deskripsi | Dampak |
|---|---|---|
| **Active Response Integration** | Menghubungkan keputusan "Approve" ke eksekusi blokir IP pada WAF/firewall (iptables, Cloudflare, Wazuh Active Response) | Menutup loop SOAR — agent bukan hanya investigasi, tapi juga mitigasi |
| **Benchmark Dashboard** | Visualisasi metrik Agent vs Baseline (data sudah tersedia di backend `/api/benchmark`) | Membuktikan nilai AI secara kuantitatif kepada manajemen |
| **Export PDF Laporan Eksekutif** | Laporan satu halaman per insiden untuk CISO/auditor/regulator | Kepatuhan terhadap UU PDP dan standar audit |
| **Multi-tenant SOC** | Dukungan untuk beberapa organisasi dalam satu deployment | Skalabilitas untuk MSSP dan konglomerat |
| **Threat Intelligence Feed** | Integrasi dengan VirusTotal, AbuseIPDB, Shodan untuk enrichment IP | Menambah kedalaman investigasi dengan data eksternal |
| **RBAC** | Role-Based Access Control (junior/senior analyst, manager) | Enterprise access governance |

---

### Bagian 9: Tautan ✍️

| Item | URL |
|---|---|
| Dashboard GTNIC SOAR (Live) | `https://gtnic-hackwitgoh.vercel.app/` |
| Lab OWASP Juice Shop (Live) | `https://juice.flummox.cloud/` |
| Repositori GitHub | [pastikan sudah public sebelum submit] |
| Video Demo (YouTube/Drive) | [harus dibuat dan diupload malam ini] |

---

## 5. ANALISIS SKOR PER-KRITERIA JURI

| # | Kriteria Penilaian | Bobot | Estimasi Skor | Analisis |
|---|---|:---:|:---:|---|
| 1 | **Kapabilitas dan Otonomi Agen** | **25%** | **9/10** | ✅ Agent benar-benar otonom: tool calling loop multi-putaran, pilih tool sendiri, buat keputusan status (confirmed/likely/uncertain/false_positive), fallback otomatis jika LLM offline. **Bukan wrapper.** |
| 2 | **Penalaran, Perencanaan, dan Pengambilan Keputusan** | **15%** | **8/10** | ✅ System prompt mengatur aturan bukti; validator menerapkan aturan deterministik (min 2 tool, pro≥2 untuk confirmed); claim guard menghapus klaim tanpa bukti; reasoning terlihat di tool trace. |
| 3 | **Penggunaan Alat dan Eksekusi Tindakan** | **15%** | **9/10** | ✅ 4 tool berbeda via Vertex AI Function Calling. Setiap tool call terekam (input/output/durasi/status). Transisi antar-tool otomatis. Facts dari tool digunakan sebagai `evidence_ref`. |
| 4 | **Arsitektur Teknis dan Rekayasa Sistem** | **15%** | **8/10** | ✅ Modular (services/api/schemas), PostgreSQL+pgvector+HNSW, Docker Compose 6 containers, CI/CD GitHub Actions, auth berlapis, graceful fallback, skema DB 4 tabel. |
| 5 | **Inovasi dan Kreativitas** | **10%** | **8/10** | ✅ Anti-halusinasi deterministik (jarang ada), Pro vs Contra Evidence (jarang ada di produk SOC manapun), Benchmark Agent vs Baseline. |
| 6 | **Dampak Masalah dan Nilai Bisnis** | **10%** | **9/10** | ✅ Cybersecurity = kebutuhan enterprise paling kritis. Metrik terukur: 25 menit → 3-8 detik, IBM: hemat USD 2,2 juta/insiden, Indonesia butuh (5,5 miliar serangan/tahun). |
| 7 | **Pengalaman dan Kemudahan Pengguna** | **5%** | **7/10** | ✅ Dark-theme SOC dashboard profesional, real-time 3s polling, filter/search. ⚠️ Belum ada onboarding/tutorial in-app, belum ada export. |
| 8 | **Demonstrasi, Presentasi, dan Dokumentasi** | **5%** | **8/10** | ✅ README lengkap, Panduan Penggunaan 200+ baris, Swagger docs, E2E test 13 skenario, CI/CD. ⚠️ Video demo masih harus dibuat. |

### Estimasi Total Skor Tertimbang:

$$\text{Skor} = (9 \times 25) + (8 \times 15) + (9 \times 15) + (8 \times 15) + (8 \times 10) + (9 \times 10) + (7 \times 5) + (8 \times 5)$$
$$= 225 + 120 + 135 + 120 + 80 + 90 + 35 + 40 = 845 / 1000$$

### **Estimasi: ~84,5/100** → Strong Contender untuk Juara 1

---

## 6. CHECKLIST PENGUMPULAN (DEADLINE: 10 November 2026, 23:59 WIB)

- [ ] Proposal PDF (maks 15 halaman, format sesuai ketentuan)
- [ ] Video Demo YouTube/Drive (3-5 menit, akses publik)
- [ ] Repositori GitHub (akses publik)
- [ ] Link Dashboard Live: `https://gtnic-hackwitgoh.vercel.app/`
- [ ] Surat Pernyataan Keaslian Karya
- [ ] Logo GTNIC 2026 di cover proposal
- [ ] Nama file: `GTNIC2026_AIAgent_[NamaTim].pdf`
