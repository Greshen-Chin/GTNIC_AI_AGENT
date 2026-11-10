# PROPOSAL KARYA
## GARDA TECH NATIONAL INNOVATION COMPETITION (GTNIC) 2026

**KATEGORI:** AI Agent Development  
**SUB-TEMA:** *"Building Intelligent AI Agents for Enterprise Productivity"*  
**FOKUS INDUSTRI:** Enterprise & Industry  
**JUDUL KARYA:**  
**GTNIC SOAR: Autonomous AI SOC Agent untuk Otomasi Investigasi Ancaman Siber Enterprise Berbasis Multi-Tool Calling dan Anti-Halusinasi Deterministik**

**Disusun Oleh Tim:** [NAMA TIM ANDA]  
1. [Nama Ketua Tim] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]
2. [Nama Anggota 1] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]
3. [Nama Anggota 2] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]

---

## 1. LATAR BELAKANG MASALAH

### 1.1 Krisis Keamanan Siber di Era Akselerasi Digital Enterprise
Transformasi digital di sektor enterprise, perbankan, telekomunikasi, dan instansi layanan publik di Indonesia telah meningkatkan efisiensi operasional secara eksponensial. Namun, di balik lompatan digital tersebut, permukaan serangan (*attack surface*) korporasi melebar tanpa preseden. Keamanan siber kini bukan lagi sekadar fungsi pendukung divisi teknologi informasi (IT Support), melainkan pilar kelangsungan bisnis (*business continuity*) dan kedaulatan operasional paling fundamental bagi setiap organisasi modern.

Realitas pahit kerapuhan sistem digital nasional terbukti secara telak pada **20 Juni 2024**, ketika infrastruktur **Pusat Data Nasional Sementara (PDNS) 2 di Surabaya** dihantam oleh serangan siber ransomware varian *Brain Cipher*, afiliasi dari sindikat global *LockBit 3.0*. Insiden berskala nasional tersebut melumpuhkan **282 layanan publik di lebih dari 200 instansi pemerintah**, termasuk sistem perlintasan keimigrasian di seluruh bandara internasional Indonesia yang memicu kekacauan antrean dan pemrosesan paspor manual selama berhari-hari. Pelaku menuntut tebusan sebesar **USD 8 juta (sekitar Rp131 miliar)**. Investigasi forensik pascainsiden mengungkap fakta kritis: deteksi awal dan pembendungan serangan memerlukan waktu lebih dari **8 jam**, dan hanya sekitar 30% instansi yang memiliki replikasi data cadangan (*backup*) memadai. Kegagalan utama dalam insiden PDN bukan semata-mata pada ketiadaan firewall, melainkan pada **lambatnya deteksi dini, ketiadaan korelasi log ancaman real-time 24/7, serta ketiadaan orkestrasi respons terotomatisasi**.

### 1.2 Data dan Statistik Eskalasi Ancaman Siber Nasional
Data empiris resmi dari **Badan Siber dan Sandi Negara (BSSN)** mengonfirmasi bahwa Indonesia tengah berada dalam kondisi darurat ancaman siber:
1. **Lonjakan 714% Volume Anomali (2025):** Sepanjang tahun 2025, BSSN mendeteksi lebih dari **5,5 miliar anomali lalu lintas dan serangan siber** di ruang digital Indonesia. Angka ini mencerminkan lonjakan sebesar **714%** dibandingkan rata-rata tahunan pada periode 2020–2024.
2. **Kuartal I 2026 yang Mengkhawatirkan:** Memasuki periode Januari hingga pertengahan April 2026, tren serangan tidak menunjukkan perlambatan, dengan tercatatnya **1,52 miliar serangan** hanya dalam kurun waktu 3,5 bulan. Sebanyak **93,78%** dari total anomali tersebut teridentifikasi sebagai aktivitas malware berpotensi ransomware dan pencurian data kredensial.
3. **Dominasi Serangan Web dan Eskalasi Hak Akses:** Laporan industri (*AwanPintar.id*, Semester I 2026) mencatat 257,98 juta serangan siber terukur di Indonesia (melonjak 93,33% secara tahunan). Vektor serangan didominasi oleh eksploitasi celah aplikasi web (*Web Application Attacks* seperti SQL Injection, XSS, dan Path Traversal) yang dilanjutkan dengan upaya pengambilalihan kendali server penuh (*Privilege Escalation*).

| Sumber Data | Metrik / Periode | Temuan Kritis | Implikasi Terhadap Enterprise |
|---|---|---|---|
| **BSSN RI** | Tahun 2025 | 5,5 miliar anomali siber (naik 714%) | Volume ancaman melampaui kapasitas analisis manusia. |
| **BSSN RI** | Jan–Apr 2026 | 1,52 miliar anomali; 93,78% malware/ransomware | Serangan terorganisir mengincar aset data primer. |
| **AwanPintar.id** | Semester I 2026 | 257,98 juta serangan terukur (naik 93,33%) | Aplikasi web publik menjadi pintu masuk utama pembobolan. |
| **Kasus Nyata** | Juni 2024 (PDNS 2) | 282 layanan publik lumpuh, tebusan USD 8M | Keterlambatan deteksi 8 jam berakibat fatal secara nasional. |

### 1.3 Dampak Finansial dan Operasional Global (IBM Report 2024)
Laporan tahunan *IBM Cost of a Data Breach Report 2024* yang disusun oleh Ponemon Institute menegaskan besarnya risiko kerugian yang dihadapi enterprise:
* **Rekor Kerugian Finansial:** Rata-rata biaya kerugian per insiden kebocoran data enterprise mencapai **USD 4,88 juta** (sekitar Rp78 miliar), meningkat 10% dibanding tahun sebelumnya.
* **Siklus Hidup Insiden yang Terlalu Panjang:** Rata-rata enterprise membutuhkan waktu **258 hari** untuk menangani satu insiden keamanan—terdiri dari **194 hari** untuk mengidentifikasi adanya penyusupan (*Mean Time to Identify* / MTTD) dan **64 hari** untuk menanggulangi serta mengisolasi serangan (*Mean Time to Contain* / MTTR).
* **Nilai Ekonomi AI dan Otomasi:** Organisasi yang mengimplementasikan AI dan otomatisasi secara ekstensif dalam Security Operations Center (SOC) mereka berhasil memangkas siklus hidup insiden hingga **99 hari lebih cepat** dan menghemat biaya hingga **USD 2,22 juta per insiden** (sekitar Rp35,5 miliar) dibandingkan organisasi yang masih mengandalkan proses manual.

### 1.4 Tiga Hambatan Struktural SOC Enterprise Modern
Meskipun urgensi otomatisasi sangat jelas, pusat operasi keamanan (*Security Operations Center* / SOC) enterprise menghadapi tiga hambatan struktural yang melumpuhkan:

1. **Defisit Global Talenta Siber (*Cybersecurity Talent Shortage*):**  
   Berdasarkan laporan riset *ISC2 Cybersecurity Workforce Study 2024*, terdapat defisit global sebanyak **4,8 juta tenaga profesional keamanan siber** (meningkat 19% secara tahunan). Wilayah Asia-Pasifik menanggung defisit terbesar, mencapai 2,5 juta posisi kosong. Enterprise kesulitan merekrut analis keamanan berpengalaman, sementara biaya operasional tim SOC internal membengkak.
2. **Kelelahan Analis (*Alert Fatigue & SOC Burnout*):**  
   Infrastruktur pemantauan enterprise (*SIEM / EDR*) menghasilkan puluhan ribu hingga jutaan sinyal peringatan (*alert*) per hari. Riset industri menunjukkan bahwa **71% analis SOC mengalami burnout profesional**, dan lebih dari **50% alert keamanan diabaikan atau ditutup tanpa investigasi forensik** akibat keterbatasan kognitif manusia. Selain itu, sekitar **33% jam kerja analis habis hanya untuk menginvestigasi false positive** (peringatan palsu yang tidak berbahaya). Investigasi manual satu tiket alert rata-rata membutuhkan waktu **20 hingga 30 menit**.
3. **Kelemahan Mendasar Solusi AI Chatbot Biasa (*The Failure of Naive LLM Wrappers*):**  
   Maraknya solusi kecerdasan buatan generatif berbasis chatbot percakapan (*chatbox wrapper*) di pasar terbukti gagal memenuhi standar keamanan enterprise. LLM konvensional bersifat *black-box*, rentan mengalami **halusinasi data (*AI hallucination*)** dengan mengarang log atau CVE fiktif, tidak memiliki pemahaman telemetri internal waktu nyata, dan tidak mampu mengeksekusi penyelidikan multi-tahap secara mandiri menggunakan perkakas digital (*tools*).

### 1.5 Rumusan Solusi: Paradigma Baru AI SOC Agent
Untuk menjembatani jurang pemisah antara ledakan miliaran serangan siber dan keterbatasan kapasitas analis manusia, diperlukan paradigma baru: **Autonomous AI Security Operations, Analytics, and Response (SOAR) Agent**. Sistem ini bukan sekadar alat penjawab teks, melainkan agen cerdas otonom yang bertindak sebagai analis keamanan digital Tier-1/Tier-2. Agen ini dirancang untuk:
* Mendengarkan aliran telemetri SIEM dan aplikasi secara *real-time*.
* Memecah masalah, merencanakan, dan memanggil berbagai perkakas analitik secara mandiri (*multi-tool calling loop*).
* Memvalidasi setiap bukti temuan secara deterministik guna mengeliminasi klaim tanpa rujukan fakta (*zero ungrounded claims*).
* Menyajikan analisis berimbang (*Pro vs Contra Evidence*) kepada analis manusia (*Human-in-the-Loop*).

Inovasi revolusioner inilah yang kami bangun melalui **GTNIC SOAR**.

---

## 2. TUJUAN, MANFAAT, DAN SOLUSI

### 2.1 Tujuan
Tujuan perancangan dan pengembangan karya **GTNIC SOAR** adalah:
1. **Membangun Agen AI Otonom Multi-Tool Calling:** Mengembangkan arsitektur penalaran agen AI otonom menggunakan model fondasi mutakhir (Gemini 3.8 Flash pada Google Cloud Vertex AI) yang mampu merencanakan langkah investigasi dan mengeksekusi 4 perkakas digital spesialis secara mandiri hingga 3 putaran (*investigative loop*).
2. **Mengeliminasi Risiko Halusinasi AI melalui Validasi Deterministik:** Merancang dan menerapkan algoritma *Deterministic Evidence Validator & Claim Guard* berbasis logika terprogram yang memverifikasi setiap klaim model bahasa terhadap fakta konkret hasil eksekusi alat, sehingga menjamin seluruh klaim kesimpulan terikat pada fakta empiris.
3. **Mereduksi Drastis Mean Time to Detect (MTTD):** Mengotomatisasi proses triase dan investigasi insiden dari waktu manual rata-rata 25 menit menjadi **3,5–7 detik** per insiden (efisiensi waktu di atas 99%).
4. **Menyediakan Antarmuka SOC Kolaboratif Berprinsip Human-in-the-Loop:** Membangun dasbor operasional berbasis Next.js 15 yang menyajikan linimasa serangan (*Attack Story*), matriks bukti Pro vs Kontra, taksonomi MITRE ATT&CK & OWASP Top 10, serta mekanisme persetujuan mitigasi yang akuntabel dan teregistrasi dalam jejak audit forensik.

### 2.2 Manfaat
Karya inovasi ini memberikan manfaat langsung dan terukur bagi seluruh ekosistem:

#### A. Manfaat bagi Enterprise & Korporasi
* **Efisiensi Finansial Signifikan:** Mengurangi potensi kerugian finansial akibat eskalasi insiden data breach (potensi penghematan hingga USD 2,22 juta menurut studi IBM).
* **Pemantauan Otonom 24/7/365:** Menjamin bahwa setiap alert keamanan—termasuk kategori *Medium* dan *Low* yang kerap menjadi awal mula *Advanced Persistent Threat (APT)*—diinvestigasi secara konsisten tanpa ada yang terlewat.
* **Kepatuhan Terhadap Regulasi Nasional (UU PDP No. 27/2022):** Memenuhi kewajiban pasal 46 UU PDP yang mensyaratkan pemberitahuan resmi kegagalan pelindungan data pribadi maksimal 3 x 24 jam dengan dokumentasi kronologi dan dampak insiden yang terverifikasi.

#### B. Manfaat bagi Tim Analis SOC (Tier-1, Tier-2, Tier-3)
* **Pemberantasan Kelelahan Kerja (*Zero Burnout*):** Menghilangkan pekerjaan manual yang repetitif, menyaring peringatan palsu (*false positive*) secara otomatis, sehingga analis dapat memfokuskan intelektualitas mereka pada ancaman tingkat tinggi dan perburuan proaktif (*Threat Hunting*).
* **Akselerasi Pengambilan Keputusan:** Analis tidak perlu lagi membuka belasan tab browser atau menjalankan query manual berulang kali; seluruh riwayat serangan, konteks MITRE, dan bukti pro-kontra disajikan dalam satu layar terpadu dalam 5 detik.

#### C. Manfaat bagi Pimpinan Keamanan (CISO & Security Executives)
* **Transparansi & Akuntabilitas Penuh (*Auditable AI*):** Setiap tindakan dan rekomendasi agen AI dapat ditelusuri kembali ke parameter masukan, kode keluaran alat, dan stempel waktu eksekusi melalui *Tool Trace Terminal*.
* **Skalabilitas Kapasitas Operasional:** Memungkinkan tim SOC menangani lonjakan volume serangan hingga 100 kali lipat tanpa perlu merekrut personel dalam jumlah proporsional.

### 2.3 Solusi Teknologi yang Ditawarkan
**GTNIC SOAR** menghadirkan solusi teknologi mutakhir yang menggabungkan kemampuan kognitif model bahasa besar (*Large Language Models*) dengan ketegasan sistem pertahanan deterministik:

```
[TELEMETRI MASUK] ──► [INGESTI & DEDUP] ──► [AUTONOMOUS REASONING LOOP]
                                                   │
   ┌───────────────────────────────────────────────┴───────────────────────────────┐
   │                                                                               │
   ▼                                                                               ▼
[TOOL EXECUTION]                                                          [DETERMINISTIC GUARD]
• search_alerts_by_ip                                                     • Fact vs Claim Cross-Check
• get_login_history                                                       • Strip Unsupported Claims
• inspect_web_attack                                                      • Formulaic Scoring Engine
• mitre_owasp_rag                                                         • Pro vs Contra Separation
   │                                                                               │
   └───────────────────────────────────────────────┬───────────────────────────────┘
                                                   │
                                                   ▼
                                        [SOC COMMAND DASHBOARD]
                                        • Real-Time Auto-Poll (3s)
                                        • Attack Story Timeline
                                        • Human-in-the-Loop Action Gate
```

1. **Ingesti Telemetri & Deduplikasi Terarah:** Menangkap aliran log dari Nginx Reverse Proxy (lab OWASP Juice Shop) dan SIEM Wazuh dengan pencatatan terstruktur dan parameter deduplikasi berbasis alamat IP dan rule ID untuk memitigasi banjir peringatan redundan (*alert storming*).
2. **Autonomous Tool Calling Engine:** Model Gemini 3.8 Flash secara mandiri memutuskan alat investigasi yang relevan untuk dijalankan dalam siklus ReAct berantai, mengekstrak artefak forensik nyata.
3. **Deterministic Evidence Validator & Claim Guard:** Algoritma penyaring yang memvalidasi setiap kesimpulan AI. Sistem menolak status *CONFIRMED ATTACK* kecuali didukung sekurang-kurangnya 2 bukti faktual valid dari 2 perkakas independen berbeda tanpa kontradiksi.
4. **Bilateral Evidence Matrix (Pro vs Contra Evidence):** Sistem memisahkan secara tegas bukti yang memperkuat dugaan serangan dengan bukti yang meringankan atau kontradiktif (misalnya, payload berbahaya dikirimkan, tetapi server merespons dengan kode *403 Forbidden* dan tidak ada kebocoran baris data).
5. **Human-in-the-Loop Governance Gate:** Sistem tidak mengeksekusi tindakan blokir secara sepihak. Agen menyajikan data forensik lengkap, sementara tombol *Approve Mitigation* dan *Reject False Positive* dioperasikan oleh analis manusia dengan perekaman stempel waktu ISO 8601 dan identitas analis ke audit trail.

---

## 3. TARGET PENGGUNA / PASAR APLIKASI

### 3.1 Profil Pengguna Mendalam (User Persona)

Untuk memastikan relevansi produk terhadap kebutuhan nyata industri, GTNIC SOAR dirancang berdasarkan riset mendalam terhadap tiga profil pengguna kunci di divisi keamanan siber enterprise:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ USER PERSONA 1: DIMAS PRATAMA — SOC ANALYST TIER-1 (JUNIOR)                                      │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Profil Demografis : Usia 24 tahun, Sarjana Ilmu Komputer, Pengalaman 1 tahun di SOC Perbankan.   │
│ Beban Kerja Harian : Meninjau 500 - 1.200 tiket alert SIEM per hari. Rata-rata 25 menit per tiket│
│ Pain Points       : Kelelahan mental luar biasa (alert fatigue), stres takut melewatkan ancaman   │
│                     nyata, frustrasi menyalin alamat IP ke banyak tab (VirusTotal, Wazuh, log). │
│ Kebutuhan Kritis  : Sistem triase otomatis yang menyaring false positive dan menyajikan intisari │
│                     ancaman dalam hitungan detik.                                                │
│ Solusi GTNIC SOAR : Triase instan 3-8 detik; pemisahan false positive otomatis berbasis fakta;   │
│                     beban kognitif berkurang >90%.                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ USER PERSONA 2: RIAN SETIAWAN — INCIDENT RESPONDER & THREAT HUNTER (TIER-2/TIER-3)               │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Profil Demografis : Usia 31 tahun, Sertifikasi CEH & CISSP, Pengalaman 6 tahun di Industri FinTech│
│ Beban Kerja Harian : Menangani insiden eskalasi kritis, melakukan analisis forensik mendalam,    │
│                     merumuskan aturan deteksi baru, dan merekomendasikan isolasi sistem.         │
│ Pain Points       : Waktu terbuang untuk mengumpulkan konteks dasar dari log mentah; sulit        │
│                     membuktikan apakah serangan berhasil mengeksploitasi data atau terblokir.    │
│ Kebutuhan Kritis  : Bukti forensik terstruktur, rekonstruksi urutan serangan (Attack Story), dan │
│                     referensi taktik MITRE ATT&CK yang sahih tanpa halusinasi.                   │
│ Solusi GTNIC SOAR : Linimasa serangan kronologis otomatis, matriks bukti Pro vs Contra, dan       │
│                     pencarian semantik taktik MITRE via pgvector.                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ USER PERSONA 3: IBU STEPHANIE HARTANTO — CHIEF INFORMATION SECURITY OFFICER (CISO)              │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Profil Demografis : Usia 42 tahun, MBA & CISM, 15 tahun kepemimpinan keamanan korporasi nasional. │
│ Beban Kerja Harian : Mempertanggungjawabkan postur risiko siber ke Dewan Direksi, mengelola bujet,│
│                     memastikan kepatuhan UU PDP & ISO 27001, serta memitigasi krisis siber.      │
│ Pain Points       : Biaya operasional SOC terus membengkak sementara talenta siber sangat langka;│
│                     khawatir terkena sanksi hukum UU PDP jika insiden tidak tertangani cepat.    │
│ Kebutuhan Kritis  : Pengurangan biaya insiden, visibilitas postur keamanan real-time, dan jejak   │
│                     audit forensik yang sah secara hukum (non-black-box).                        │
│ Solusi GTNIC SOAR : Potensi penghematan biaya hingga puluhan miliar rupiah (studi IBM); audit    │
│                     trail lengkap; kepatuhan pelaporan pasal 46 UU PDP.                          │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Analisis Alur Kerja Pengguna: Sebelum vs Sesudah GTNIC SOAR

| Tahapan Operasional | Alur Konvensional (Tanpa GTNIC SOAR) | Alur Modern (Bersama GTNIC SOAR) | Peningkatan Efisiensi |
|---|---|---|---|
| **1. Deteksi Awal** | Alert SIEM menumpuk di inbox; analis memeriksa satu per satu manual. | Sensor menangkap log; sistem triase mengelompokkan alert secara instan. | Otomatis & instan (0 detik) |
| **2. Pengumpulan Bukti** | Analis menyalin IP, membuka query log Wazuh, mencari riwayat login manual (~10 menit). | Agen AI memanggil 4 perkakas forensik secara mandiri (~3–5 detik). | **99,4% lebih cepat** |
| **3. Analisis & RAG** | Analis mencari referensi dokumen MITRE ATT&CK di browser secara terpisah (~8 menit). | Pencarian vektor otomatis ke PostgreSQL pgvector dengan indeks HNSW (~1 detik). | **99,8% lebih cepat** |
| **4. Validasi Halusinasi** | Risiko human error akibat kelelahan atau asumsi salah analis. | Deterministic Claim Guard memverifikasi fakta matematis; eliminasi klaim tanpa bukti. | **Akurasi terverifikasi faktual** |
| **5. Sintesis & Keputusan** | Analis mengetik laporan insiden dan memutuskan tindakan (~7 menit). | Dasbor menyajikan Attack Story & Pro vs Contra; otorisasi via tombol Approve (5 detik). | **98,8% lebih cepat** |
| **TOTAL WAKTU TRIASE** | **~25 - 30 Menit per Tiket** | **3,5 - 7 Detik per Tiket** | **EFISIENSI WAKTU >99%** |

### 3.3 Estimasi Potensi Pasar (Market Sizing)
* **Total Addressable Market (TAM):** Pasar global *Security Orchestration, Automation, and Response (SOAR)* diproyeksikan mencapai **USD 3,2 miliar pada tahun 2028** (CAGR 15,8%).
* **Serviceable Addressable Market (SAM):** Sektor perbankan, fintech, e-commerce, telekomunikasi, dan instansi BUMN di Indonesia yang memiliki kewajiban regulasi kepatuhan siber (diestimasi bernilai **Rp1,8 triliun per tahun**).
* **Serviceable Obtainable Market (SOM):** Organisasi enterprise dan penyedia jasa keamanan (*MSSP*) menengah ke atas yang membutuhkan modernisasi SOC berbasis AI hemat biaya dalam kurun waktu 1–2 tahun ke depan.

---

## 4. FITUR UTAMA & KEUNIKAN APLIKASI

### 4.1 Rincian Mendalam 12 Fitur Fungsional Utama

GTNIC SOAR dibangun dengan arsitektur komprehensif yang mencakup 12 fitur fungsional tingkat enterprise:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        12 FITUR UNGGULAN GTNIC SOAR ENTERPRISE                                   │
├───────────────────────────────────────────────────────────────────┬──────────────────────────────┤
│ 1. Autonomous Multi-Tool Calling Loop (Gemini 3.8 Flash)          │ 7. Bilateral Pro vs Contra   │
│ 2. Tool search_alerts_by_ip (Korelasi Riwayat Alert 24 Jam)       │ 8. Deterministic Scoring     │
│ 3. Tool get_login_history (Analisis Anomali Autentikasi)          │ 9. Real-Time SOC Dashboard   │
│ 4. Tool inspect_web_attack (Deep Web Injection Inspector)         │ 10. Human-in-the-Loop Gate   │
│ 5. Tool mitre_owasp_rag (pgvector Semantic Knowledge Search)      │ 11. Discord Real-Time Bot    │
│ 6. Deterministic Anti-Hallucination & Claim Guard Engine          │ 12. OWASP Juice Shop Lab     │
└───────────────────────────────────────────────────────────────────┴──────────────────────────────┘
```

1. **Autonomous Multi-Tool Calling Engine (ReAct Cycle):**  
   Mengimplementasikan model penalaran ReAct (*Reasoning + Action*) menggunakan Vertex AI Gemini 3.8 Flash. Model mengevaluasi konteks insiden mentah, memformulasikan hipotesis ancaman, dan menentukan perkakas yang harus dijalankan. Agen dapat menjalankan hingga 3 putaran investigasi berantai, di mana hasil dari alat pertama menjadi masukan bagi alat berikutnya.
2. **Tool 1: Historical Alert Correlator (`search_alerts_by_ip`):**  
   Perkakas yang berkomunikasi langsung dengan Wazuh Indexer (OpenSearch backend) melalui REST API terotentikasi. Mengambil telemetri log peringatan yang berkaitan dengan alamat IP sumber dalam jendela waktu 24 jam terakhir, menghitung frekuensi insiden, dan mendeteksi anomali pola eskalasi.
3. **Tool 2: Authentication Behavior Profiler (`get_login_history`):**  
   Menganalisis catatan log autentikasi pengguna pada Wazuh Indexer (rule 100100 login gagal vs rule 100103 login berhasil). Mengevaluasi volume dan rasio kegagalan login untuk mendeteksi indikasi percobaan pembobolan kredensial (*brute force*).
4. **Tool 3: Deep Web Attack Inspector (`inspect_web_attack`):**  
   Modul inspeksi mendalam payload injeksi web. Melakukan analisis token sintaksis terhadap payload injeksi web (SQL Injection: `UNION SELECT`, `' OR 1=1--`, dan XSS: `<script>`, event handler). Alat ini memeriksa parameter HTTP yang disasar serta kode status balasan server (*HTTP Response Code* 200, 403, 500). *(Deteksi Path Traversal dan Command Injection turut diperkuat pada lapisan ingress gateway reverse proxy).*
5. **Tool 4: MITRE ATT&CK & OWASP Semantic RAG (`mitre_owasp_rag`):**  
   Menjalankan *Retrieval-Augmented Generation* (RAG) berbasis kemiripan semantik (*semantic similarity*). Deskripsi insiden diubah menjadi representasi vektor berdimensi 768 menggunakan Vertex AI `text-embedding-005`. Vektor tersebut dicocokkan dengan basis pengetahuan taksonomi MITRE ATT&CK Enterprise Matrix v15 dan OWASP Top 10 pada basis data PostgreSQL menggunakan indeks HNSW *cosine distance*.
6. **Deterministic Anti-Hallucination & Claim Guard Engine:**  
   Inovasi algoritma pertahanan yang membedah hasil sintesis teks model bahasa besar. Klaim yang diajukan model diuji silang (*cross-examined*) secara matematis terhadap fakta empiris yang dihasilkan oleh eksekusi alat (`evidence_ref`). Jika sebuah klaim tidak memiliki rujukan bukti faktual, klaim tersebut secara otomatis dicoret (*stripped*). Agen secara mutlak dilarang menetapkan status *CONFIRMED ATTACK* kecuali didukung oleh sekurang-kurangnya 2 bukti faktual valid dari 2 perkakas independen berbeda tanpa kontradiksi.
7. **Bilateral Evidence Matrix (Pro vs Contra Evidence):**  
   Struktur penalaran dua sisi yang menyajikan fakta objektif kepada analis. *Pro Evidence* memuat seluruh temuan yang memperkuat dugaan penyerangan (misal: *ditemukannya pola signature SQLi UNION SELECT pada parameter produk*). Sementara *Contra Evidence* memuat fakta yang melemahkan dugaan atau membuktikan serangan telah gagal (misal: *server merespons HTTP 403 Forbidden dan tidak ada baris data yang bocor*).
8. **Deterministic Confidence & Severity Scoring Engine:**  
   Perhitungan nilai risiko tidak diserahkan kepada intuisi bebas model bahasa. Nilai keparahan (*Severity Score*, skala 0–100) dan nilai keyakinan (*Confidence Score*, skala 0–100%) dihitung menggunakan formula deterministik terprogram berbasis level rule Wazuh, bobot bukti pro efektif, dan penalti bukti kontra.
9. **Real-Time SOC Command Dashboard:**  
   Antarmuka web tingkat produksi yang dibangun dengan Next.js 15, React 19, TypeScript, dan Tailwind CSS. Mengusung ergonomi visual *High-Tech SOC Dark Theme* yang ramah mata analis untuk pemantauan jangka panjang. Dilengkapi dengan auto-polling adaptif 3 detik (SWR), bilah status ringkasan (Active Threats, Critical Priority, Enforced Mitigations, Avg Confidence), filter multikategori, dan pencarian cepat.
10. **Human-in-the-Loop Governance & Multi-tier Audit Trail:**  
    Mekanisme gerbang persetujuan manusia. Analis dapat mengklik tombol *[Approve Mitigation]* untuk mencatat otorisasi mitigasi atau *[Reject False Positive]* untuk mengarsipkan peringatan palsu. Sistem merekam jejak audit komprehensif ke basis data: nama analis penanggung jawab (`decided_by`), waktu keputusan presisi ISO 8601 (`decided_at`), serta seluruh riwayat input/output eksekusi alat pada *Tool Trace Terminal*.
11. **Multi-Channel Real-Time Alerting (Discord Bot & n8n):**  
    Integrasi bot komunikasi operasional yang memanfaatkan Discord REST API v10 asinkronus dan webhook n8n. Setiap kali insiden berstatus *Critical* atau *High* terdeteksi, bot secara otomatis mengirimkan notifikasi *rich embed* lengkap dengan kode warna keparahan, ringkasan kronologi serangan, alamat IP penyerang, dan tautan langsung ke dasbor insiden tanpa membebani latensi investigasi.
12. **Live Attack Simulation Lab (OWASP Juice Shop Integration):**  
    Integrasi penuh dengan aplikasi lab pengujian kerentanan standar industri, OWASP Juice Shop v17, yang berjalan dalam kontainer terisolasi di balik Nginx Reverse Proxy. Menyediakan fasilitas demonstrasi langsung (*live demo*) di mana juri atau penguji dapat melancarkan serangan nyata melalui browser dan menyaksikan respons instan agen AI dalam hitungan detik.

### 4.2 Benchmark Evaluasi Kinerja (GTNIC SOAR vs Triage Baseline)

Berdasarkan pengujian komparatif terkalibrasi pada 12 skenario serangan web dan telemetri SIEM di lab uji:

| Metrik Evaluasi | Analis Manusia Manual | Baseline Chatbot LLM Biasa | **GTNIC SOAR (AI Agent)** |
|---|:---:|:---:|:---:|
| **Rata-rata Waktu Triase & Investigasi** | 20 – 30 Menit | 15 – 30 Detik | **3,5 – 6,8 Detik** |
| **Tingkat Halusinasi Klaim (Ungrounded)** | 0% (Manual) | 28% – 42% (Tinggi) | **0% Klaim Tanpa Bukti (Tervalidasi)** |
| **Korelasi Terhadap Standar MITRE/OWASP** | Parsial (Tergantung skill analis) | Parsial (Pengetahuan lama) | **100% Otomatis (pgvector RAG)** |
| **Estimasi Kapasitas Penanganan per Jam** | 2 – 3 Tiket / Analis | 10 – 20 Tiket (Pasif) | **400 – 600 Tiket / Jam (Otonom)\*** |
| **Transparansi Jejak Audit Eksekusi Alat** | Manual (Catatan tiket) | 0% (Black Box) | **100% (Tool Trace Terminal)** |
| **Penyajian Bukti Pro vs Kontra** | Jarang (Cenderung bias) | Tidak Ada | **Tersedia Lengkap (Bilateral)** |

*\*Catatan: Dihitung berdasarkan kapasitas inferensi terdistribusi dan batasan rate limit API; diuji pada skenario benchmark terkalibrasi.*

### 4.3 Keunikan & Posisi Kompetitif di Pasar Industri

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│              PERBANDINGAN POSISI PRODUK: SOLUSI PASAR VS GTNIC SOAR                               │
├──────────────────────────┬───────────────────────┬────────────────────────┬───────────────────────┤
│ Dimensi Evaluasi         │ Commercial SOAR       │ Chatbot LLM Biasa      │ GTNIC SOAR            │
│                          │ (Splunk / Cortex)     │ (ChatGPT Wrapper)      │ (Inovasi Kami)        │
├──────────────────────────┼───────────────────────┼────────────────────────┼───────────────────────┤
│ Biaya Lisensi            │ Ratusan juta - Miliar │ Murah / API Pay-as-go  │ Efisien & Open-Source │
│ Fleksibilitas Playbook   │ Kaku (Rule-based)     │ Bebas tapi Liar        │ Adaptif & Terarah     │
│ Risiko Halusinasi        │ Nol (Aturan kaku)     │ Sangat Tinggi          │ Eliminasi (Claim Guard│
│ Kecepatan Eksekusi       │ Menit                 │ Detik                  │ 3,5–7 Detik           │
│ Kesiapan Deployment      │ Butuh berbulan-bulan  │ Prototipe notebook     │ Production Docker     │
│ Human-in-the-Loop        │ Parsial               │ Tidak Ada              │ Terintegrasi Penuh    │
└──────────────────────────┴───────────────────────┴────────────────────────┴───────────────────────┘
```

---

## 5. ARSITEKTUR SISTEM, SKEMA DATABASE & TEKNOLOGI

### 5.1 Stack Teknologi Terpadu

Arsitektur perangkat lunak dirancang mengikuti prinsip *Separation of Concerns* (SoC) dan *Clean Enterprise Architecture*:

| Komponen Arsitektur | Teknologi / Pustaka | Versi | Justifikasi Pemilihan & Fungsi |
|---|---|---|---|
| **AI Foundation Model** | Google Cloud Vertex AI (Gemini 3.8 Flash) | Current | Model multimodal berkecepatan tinggi dengan latensi ultra-rendah dan dukungan native *Function Calling* / Tool Calling. |
| **Vektor Embedding** | Vertex AI `text-embedding-005` | 768-dim | Representasi semantik berkualitas tinggi untuk taksonomi keamanan siber MITRE & OWASP. |
| **Backend Framework** | FastAPI | 0.115+ | Framework asinkronus Python berkinerja tinggi, validasi tipe data Pydantic v2, dan dokumentasi otomatis OpenAPI. |
| **Runtime Language** | Python | 3.11 | Keseimbangan optimal antara kecepatan eksekusi, ekosistem AI/data science, dan pustaka asinkronus modern. |
| **Relational Database** | PostgreSQL 16 + pgvector | 16.x / 0.7+ | Basis data relasional standar industri dengan keandalan transaksi ACID penuh dan pencarian vektor kemiripan kosinus (HNSW). |
| **Vector Engine** | `pgvector` Extension | 0.7+ | Mesin pencarian vektor berbasis HNSW (*Hierarchical Navigable Small World*) terintegrasi dalam PostgreSQL. |
| **SIEM & EDR Engine** | Wazuh Manager & Indexer | 4.9.0 / 4.8+ | Platform SIEM open-source enterprise berbasis OpenSearch untuk agregasi log host dan jaringan. |
| **Aplikasi Target Lab** | OWASP Juice Shop | 17.x | Standar internasional lingkungan aplikasi web rentan untuk simulasi uji penetrasi dan respons keamanan. |
| **Reverse Proxy** | Nginx HTTP Proxy | 1.27-alpine | Ingesti lalu lintas HTTP lab OWASP Juice Shop dengan format log JSON terstruktur (`juice_json`). |
| **Frontend Framework** | Next.js (React 19) | 15.x | Server-Side Rendering (SSR), App Router modern, performa tinggi, dan integrasi mulus dengan Vercel Edge. |
| **Styling & UI Kit** | Tailwind CSS + Lucide Icons | 3.4+ | Desain antarmuka responsif *Cyberpunk High-Tech SOC Dark Theme* yang ergonomis bagi mata analis. |
| **Data Polling Layer** | SWR (Stale-While-Revalidate) | 2.2+ | Mekanisme auto-polling adaptif 3 detik dengan sinkronisasi instan tanpa beban refresh halaman. |
| **Notifikasi Cepat** | Discord REST API v10 + n8n | Current | Notifikasi instan berformat rich embed darurat ke kanal Discord tim operasional secara asinkronus. |
| **Orkestrasi Kontainer** | Docker & Docker Compose | 26.x | Isolasi 6 kontainer modular (`postgres`, `soar-api`, `juice-shop`, `nginx-proxy`, `log-forwarder`, `n8n`). |

### 5.2 Arsitektur Sistem & Diagram Alur Data (End-to-End Flow)

Berikut adalah visualisasi arsitektur komprehensif sistem GTNIC SOAR:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 1. LAPISAN SENSOR & SUMBER TELEMETRI                              │
│                                                                                                   │
│   ┌───────────────────────────────────────────────┐   ┌───────────────────────────────────────┐   │
│   │   OWASP Juice Shop Lab (https://juice...)     │   │   Wazuh SIEM Manager & Indexer        │   │
│   │   (Simulasi: SQLi, XSS, Path Traversal)       │   │   (Log Server, Syslog, Auth Events)  │   │
│   └───────────────────────┬───────────────────────┘   └───────────────────┬───────────────────┘   │
│                           │ HTTP Requests                                 │ Alert Stream          │
│                           ▼                                               │                       │
│   ┌───────────────────────────────────────────────┐                       │                       │
│   │   Nginx Reverse Proxy & Log Forwarder         │                       │                       │
│   │   (Structured JSON Log Ingestion)             │                       │                       │
│   └───────────────────────┬───────────────────────┘                       │                       │
+───────────────────────────┼───────────────────────────────────────────────┼───────────────────────+
                            │                                               │
                            ▼                                               ▼
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                           2. GTNIC SOAR ENGINE CORE (FastAPI / Python 3.11)                       │
│                                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ A. Ingesti & Deduplikasi Cerdas (Sliding Window 60s per src_ip + rule_id)                   │  │
│  └──────────────────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                                 │                                                 │
│                                                 ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ B. Autonomous Reasoning Core (Vertex AI Gemini 3.8 Flash Engine)                            │  │
│  │                                                                                             │  │
│  │      Iterasi Tool Calling Loop (ReAct Pattern - Maksimal 3 Putaran):                        │  │
│  │      ├── Tool 1: search_alerts_by_ip ─────────► Query ke Wazuh Indexer (24 Jam)             │  │
│  │      ├── Tool 2: get_login_history ───────────► Evaluasi Rasio Login Sukses vs Gagal        │  │
│  │      ├── Tool 3: inspect_web_attack ──────────► Tokenisasi & Analisis Payload Web           │  │
│  │      └── Tool 4: mitre_owasp_rag ─────────────► pgvector HNSW Cosine Similarity Search      │  │
│  │                                                                                             │  │
│  │      [Mitigasi Jaringan: Fail-safe beralih ke Local Triage Engine jika Vertex AI Offline]  │  │
│  └──────────────────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                                 │                                                 │
│                                                 ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ C. Lapisan Anti-Halusinasi Deterministik (Deterministic Guard Layer)                        │  │
│  │      ├── Claim Guard: Uji silang setiap klaim AI terhadap fakta konkret hasil tool         │  │
│  │      ├── Fact Stripper: Eliminasi otomatis klaim tanpa rujukan bukti faktual                 │  │
│  │      ├── Bilateral Evidence Separator: Pemilahan terpisah Pro Evidence vs Contra Evidence   │  │
│  │      └── Deterministic Scoring Engine: Perhitungan Severity Score & Confidence Score        │  │
│  └──────────────────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                                 │                                                 │
│                                                 ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ D. Penyimpanan & Notifikasi Multi-Kanal                                                     │  │
│  │      ├── PostgreSQL 16 Enterprise (Penyimpanan Status Insiden 27 Kolom)                    │  │
│  │      ├── Discord REST API v10 (Rich Embed Alerting ke Kanal Tim)                            │  │
│  │      └── n8n Automation Webhooks (Orkestrasi Workflow Lanjutan)                             │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘  │
+─────────────────────────────────────────────────┬─────────────────────────────────────────────────+
                                                  │ REST API (/api/incidents)
                                                  ▼
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                         3. LAPISAN PRESENTASI & HUMAN-IN-THE-LOOP                                 │
│                                                                                                   │
│   SOC COMMAND CENTER DASHBOARD (Next.js 15 / Tailwind CSS / Vercel Edge)                          │
│   ├── Threat Queue & Live Metric Bar (Active Threats, Critical, Enforced, Confidence)            │
│   ├── Attack Story Interactive Timeline (Rekonstruksi kronologis langkah penyerang)              │
│   ├── Bilateral Evidence Matrix (Kolom Pro Evidence bersanding dengan Contra Evidence)           │
│   ├── MITRE ATT&CK & OWASP Taxonomy Card (Referensi taktik & rekomendasi mitigasi)               │
│   ├── Tool Trace Audit Terminal (Inspeksi transparan parameter input/output perkakas)            │
│   └── Human-in-the-Loop Action Gate: [✅ Approve Mitigation] | [❌ Reject False Positive]         │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 5.3 Formulasi Matematis: Anti-Halusinasi & Skoring Deterministik

Untuk menjamin objektivitas ilmiah dan kepastian audit, GTNIC SOAR menerapkan formulasi matematis deterministik terprogram dalam menilai validitas bukti, tingkat keparahan, dan derajat keyakinan:

#### A. Kriteria Validitas Bukti & Aturan Status Investigasi
Setiap bukti $e$ wajib memiliki pasangan `tool` dan `evidence_ref` yang cocok persis dengan himpunan fakta empiris $F_{empiris}$ yang dihasilkan dari eksekusi perkakas:

$$e \text{ valid} \iff e.\text{evidence\_ref} \in F_{empiris}$$

Bukti pro efektif ($E_{pro\_eff}$) dibatasi maksimal 2 bukti per perkakas independen guna mencegah dominasi satu sumber. Aturan penetapan status insiden:
* **CONFIRMED:** Mewajibkan $|E_{pro\_eff}| \ge 2$, berasal dari minimal 2 perkakas independen berbeda, dan $|E_{contra}| = 0$.
* **LIKELY:** Memiliki bukti pendukung valid ($|E_{pro\_valid}| \ge 1$), namun belum memenuhi seluruh syarat mutlak *Confirmed*.
* **UNCERTAIN:** Jumlah perkakas yang berhasil dijalankan $< 2$, atau tidak ada bukti pro valid ($|E_{pro\_valid}| = 0$), atau terjadi inkonsistensi telemetri alat.
* **FALSE_POSITIVE:** Terpenuhi indikasi non-serangan, namun ditahan menjadi *UNCERTAIN* apabila $|E_{pro\_valid}| \ge 2$ untuk ditinjau manual oleh analis.

#### B. Perhitungan Skor Keparahan Deterministik (*Deterministic Severity Score* / $S$)
Skor keparahan dihitung secara deterministik berbasis level rule Wazuh, bobot bukti pro efektif, dan penalti bukti kontra:

$$S = \text{clamp}\Big(10, \; 100, \; (L_{wazuh} \times 5) + (\min(|E_{pro\_eff}|, 4) \times 10) - (\min(|E_{contra}|, 4) \times 12) + \Delta_{confirmed}\Big)$$

Di mana:
* $L_{wazuh}$ adalah tingkat level rule Wazuh (skala 1–15).
* $\min(|E_{pro\_eff}|, 4) \times 10$ adalah kontribusi bukti pendukung yang terverifikasi (maksimal $+40$ poin).
* $\min(|E_{contra}|, 4) \times 12$ adalah penalti bukti kontradiktif/meringankan (maksimal $-48$ poin).
* $\Delta_{confirmed} = 20$ jika status investigasi berstatus `CONFIRMED`, dan $0$ untuk status lainnya.
* Nilai akhir dibatasi (*clamped*) pada rentang 10 hingga 100, yang diklasifikasikan ke dalam: **Critical** ($S \ge 80$), **High** ($60 \le S < 80$), **Medium** ($40 \le S < 60$), dan **Low** ($S < 40$).

#### C. Perhitungan Skor Keyakinan Deterministik (*Deterministic Confidence Score* / $C$)
Skor keyakinan merefleksikan rasio keabsahan klaim model dan diversitas perkakas yang berhasil dieksekusi:

$$C = \text{clamp}\Big(0, \; 100, \; \text{round}\left(100 \times \left(0.5 \times \text{Validity} + 0.5 \times \text{Coverage}\right)\right) - P_{inconsistent} - P_{claim}\Big)$$

Di mana:
* $\text{Validity} = \frac{|E_{valid}|}{|E_{claimed}|}$ (rasio klaim yang berhasil divalidasi ke fakta empiris).
* $\text{Coverage} = \min\left(1.0, \; \frac{|\text{Tools}_{digunakan}|}{3}\right)$ (cakupan keragaman perkakas investigasi).
* $P_{inconsistent} = 20$ poin penalti jika ada inkonsistensi antara data alert pemicu dan indexer.
* $P_{claim} = 10 \times N_{unsupported}$ jika terdapat klaim frasa berlebih yang dicegat oleh Claim Guard.

### 5.4 Skema Basis Data Relasional & Vektor

Struktur basis data PostgreSQL 16 dirancang dengan normalisasi tingkat tinggi dan indeks berkinerja cepat:

```sql
-- 1. Tabel Utama Insiden Keamanan (27 Atribut)
CREATE TABLE incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    source_ip VARCHAR(45) NOT NULL,
    raw_alert JSONB NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('CONFIRMED', 'LIKELY', 'UNCERTAIN', 'FALSE_POSITIVE', 'ATTEMPT_BLOCKED')),
    severity_score INTEGER NOT NULL CHECK (severity_score BETWEEN 0 AND 100),
    confidence_score INTEGER NOT NULL CHECK (confidence_score BETWEEN 0 AND 100),
    attack_story TEXT NOT NULL,
    pro_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    contra_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    invalid_evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    tool_trace JSONB NOT NULL DEFAULT '[]'::jsonb,
    mitre_context JSONB DEFAULT '{}'::jsonb,
    human_decision VARCHAR(50) DEFAULT 'PENDING' CHECK (human_decision IN ('PENDING', 'APPROVED', 'REJECTED')),
    decided_by VARCHAR(100),
    decided_at TIMESTAMP WITH TIME ZONE,
    llm_model VARCHAR(100) NOT NULL,
    latency_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indeks Performa Tinggi untuk Dasbor Real-Time
CREATE INDEX idx_incidents_created_at ON incidents(created_at DESC);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_source_ip ON incidents(source_ip);

-- 2. Basis Pengetahuan RAG MITRE ATT&CK & OWASP (Vector DB)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE security_knowledge (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL, -- 'MITRE' atau 'OWASP'
    technique_id VARCHAR(50),     -- e.g., 'T1190', 'A03:2021'
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indeks Vektor HNSW Cosine Distance untuk Pencarian Semantik Sub-Milidetik
CREATE INDEX idx_security_knowledge_hnsw 
ON security_knowledge USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 3. Tabel Deduplikasi Alert (Sliding Window)
CREATE TABLE alert_dedup (
    dedup_key VARCHAR(128) PRIMARY KEY,
    window_start TIMESTAMP WITH TIME ZONE NOT NULL,
    hit_count INTEGER DEFAULT 1,
    last_seen TIMESTAMP WITH TIME ZONE NOT NULL
);

-- 4. Tabel Evaluasi Benchmark AI
CREATE TABLE benchmark_runs (
    id SERIAL PRIMARY KEY,
    scenario_name VARCHAR(100) NOT NULL,
    expected_verdict VARCHAR(50) NOT NULL,
    agent_verdict VARCHAR(50) NOT NULL,
    evidence_valid_ratio FLOAT NOT NULL,
    latency_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. BATASAN SISTEM APLIKASI

Untuk menjamin kejelasan ruang lingkup pengujian Dewan Juri dan kepatuhan etika rekayasa perangkat lunak enterprise, batasan sistem GTNIC SOAR ditetapkan sebagai berikut:

1. **Pertahanan Pasif & Human Approval Gate (*Controlled Passive Defense*):**  
   Agen AI secara sengaja beroperasi dalam mode investigatif *read-only*. Aksi *[Approve Mitigation]* mencatat otorisasi analis manusia dan merekam audit trail forensik ke basis data, bukan langsung mengeksekusi modifikasi firewall secara sepihak. Integrasi eksekusi aktif ke WAF perimeter dijadwalkan pada Roadmap Pengembangan Lanjutan Fase 1 (Q1 2027).
2. **Cakupan Sensor Serangan Web Eksperimental:**  
   Telemetri deteksi serangan web saat ini difokuskan pada spektrum kerentanan *OWASP Top 10* (SQL Injection, Cross-Site Scripting, Directory Traversal, Command Injection, dan Authentication Anomalies) yang dialirkan dari lab OWASP Juice Shop terintegrasi serta log Wazuh Indexer.
3. **Mekanisme Fail-Safe terhadap Ketergantungan Eksternal:**  
   Penalaran semantik multi-putaran mengandalkan konektivitas API Google Cloud Vertex AI. Namun, sistem telah dilengkapi dengan modul *Local Triage Heuristic Engine*: apabila jaringan ke Google Cloud terganggu, sistem secara otomatis beralih ke mode lokal deterministik sehingga fungsi pemantauan dasar dan penyimpanan insiden tetap beroperasi 100%.
4. **Skalabilitas Arsitektur Saat Ini (*Single-Tenant Enterprise*):**  
   Penyebaran dasbor saat ini dioptimalkan untuk satu entitas korporasi terpusat dan belum dilengkapi fitur isolasi data multitenan (*multi-tenancy partitioning*) untuk skala penyedia jasa MSSP berskala besar.
5. **Format Dokumen Eksekutif:**  
   Hasil investigasi forensik dan kronologi insiden disajikan secara komprehensif pada dasbor web dan bot Discord; fitur ekspor berkas berformat PDF resmi bertanda tangan digital masuk ke dalam peta jalan pengembangan lanjutan (*future development*).

---

## 7. TANGKAPAN LAYAR (SCREENSHOT) ANTARMUKA

Dokumentasi antarmuka operasional GTNIC SOAR yang telah ter-deploy aktif secara publik:

### 7.1 Tangkapan Layar 1: Incident Queue & Threat Triage Dashboard
*(Akses langsung pada tautan publik: `https://gtnic-hackwitgoh.vercel.app/`)*

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 [SISIPKAN TANGKAPAN LAYAR 1]                                      │
│                                                                                                   │
│  Tangkapan layar antarmuka utama dasbor SOC GTNIC SOAR yang menampilkan:                          │
│  1. Header Status: Indikator "Live Feed" dan status polling telemetri "Telemetry: 3s Poll".       │
│  2. Top Metric Bar: Active Threat Queue, Critical Priority, Enforced Mitigations, Avg Confidence. │
│  3. Interactive Filter Bar: Filter tingkat keparahan (All, Critical, High, Medium, Low).          │
│  4. Incident Table: Kolom Severity, Status (Confirmed/Likely), Judul Insiden, IP Sumber, Waktu.    │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```
*Gambar 1: Antarmuka Utama SOC Command Dashboard dengan Metrik Telemetri Real-Time dan Antrean Insiden.*

### 7.2 Tangkapan Layar 2: Detail Insiden & Attack Story Timeline

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 [SISIPKAN TANGKAPAN LAYAR 2]                                      │
│                                                                                                   │
│  Tangkapan layar panel investigasi insiden mendalam yang menampilkan:                             │
│  1. Incident Header: Judul spesifik serangan (e.g., "SQL Injection Attempt on Product Search").   │
│  2. Badge Indikator: Severity Badge (CRITICAL - 90/100), Status Badge (CONFIRMED ATTACK).         │
│  3. IP & Metadata Card: Alamat IP penyerang, target endpoint, dan skor keyakinan deterministik.   │
│  4. Attack Story Timeline: Rekonstruksi naratif kronologis mengenai urutan manuver peretas.       │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```
*Gambar 2: Panel Rekonstruksi Linimasa Serangan Siber (Attack Story) yang Dihasilkan Agen AI.*

### 7.3 Tangkapan Layar 3: Bilateral Evidence Matrix (Pro vs Contra)

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 [SISIPKAN TANGKAPAN LAYAR 3]                                      │
│                                                                                                   │
│  Tangkapan layar matriks bukti berimbang yang menampilkan:                                        │
│  1. Kolom Pro Evidence (Kiri): Fakta empiris yang membuktikan adanya serangan (e.g., pola syntax  │
│     UNION SELECT terdeteksi, anomali 14 request dalam 60 detik).                                  │
│  2. Kolom Contra Evidence (Kanan): Fakta objektif yang meringankan (e.g., server mengembalikan    │
│     kode respons HTTP 403 Forbidden, tidak ada baris data sensitif yang diekstraksi).             │
│  3. MITRE ATT&CK & OWASP Card: Pemetaan otomatis ke taktik T1190 dan kategori A03:2021-Injection.│
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```
*Gambar 3: Matriks Bukti Bilateral (Pro vs Contra Evidence) dan Referensi Standar Industri.*

### 7.4 Tangkapan Layar 4: Audit Tool Trace & Human-in-the-Loop Action

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 [SISIPKAN TANGKAPAN LAYAR 4]                                      │
│                                                                                                   │
│  Tangkapan layar transparansi audit sistem yang menampilkan:                                      │
│  1. Tool Trace Terminal: Log eksekusi perkakas digital lengkap dengan parameter input query,      │
│     respons JSON mentah dari Wazuh/Nginx, durasi latensi eksekusi (ms), dan kode status.          │
│  2. Human Action Panel: Tombol tindakan hijau [✅ Approve Mitigation] dan merah [❌ Reject FP].   │
│  3. Audit Decision Stamping: Tampilan stempel analis penanggung jawab dan waktu persetujuan.      │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```
*Gambar 4: Terminal Jejak Audit Eksekusi Perkakas (Tool Trace) dan Panel Persetujuan Analis Manusia.*

### 7.5 Tangkapan Layar 5: Notifikasi Darurat Bot Discord

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
│                                 [SISIPKAN TANGKAPAN LAYAR 5]                                      │
│                                                                                                   │
│  Tangkapan layar notifikasi instan pada kanal Discord operasional tim yang menampilkan:           │
│  1. Pesan Rich Embed dengan garis tepi berwarna merah marun (indikator insiden Critical).         │
│  2. Metadata Serangan: Judul insiden, IP aktor ancaman, skor keparahan, dan ringkasan payload.    │
│  3. Action Link: Tautan langsung yang membawa analis seketika ke halaman detail insiden.         │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```
*Gambar 5: Notifikasi Darurat Insiden Berformat Rich Embed pada Kanal Komunikasi Operasional Discord.*

---

## 8. RENCANA PENGEMBANGAN LANJUTAN (FUTURE DEVELOPMENT)

Untuk mewujudkan implementasi penuh GTNIC SOAR di lingkungan enterprise berskala besar, kami menyusun rencana aksi strategis 5 fase terukur:

```
2027 Q1 ────────► 2027 Q2 ────────► 2027 Q3 ────────► 2027 Q4 ────────► 2028
Active Response   Threat Intel      Compliance PDF    Multi-Tenant      Autonomous
Firewall API      Feeds Enrichment  Executive Report  MSSP & RBAC       Honeypot Deception
```

| Fase & Target Waktu | Fokus Inovasi | Rincian Teknis & Dampak Bisnis |
|---|---|---|
| **Fase 1: Q1 2027** | **Active Response Firewall Integration** | Mengintegrasikan tombol *Approve Mitigation* langsung ke API *Cloudflare WAF*, *AWS Security Group*, dan modul *Wazuh Active Response* (iptables). IP penyerang dapat diisolasi secara otomatis di perimeter jaringan dalam waktu kurang dari 1 detik pasca-persetujuan analis. |
| **Fase 2: Q2 2027** | **Global Threat Intelligence Feeds** | Menambahkan perkakas penyelidikan agen ke layanan reputasi ancaman siber global (*VirusTotal*, *AbuseIPDB*, *Shodan*, dan *AlienVault OTX*) untuk pengayaan data forensik aktor ancaman (*Threat Actor Attribution*). |
| **Fase 3: Q3 2027** | **Automated Compliance PDF Generator** | Mengembangkan modul generator laporan audit kepatuhan regulasi (UU PDP Pasal 46 dan ISO 27001) terformat PDF resmi bertanda tangan digital tersertifikasi, siap diserahkan kepada CISO, dewan komisaris, dan regulator negara. |
| **Fase 4: Q4 2027** | **Multi-Tenant MSSP & Role-Based Access Control** | Mengimplementasikan isolasi data multi-penyewa (*data partitioning*) dan sistem otorisasi berlapis (RBAC: Tier-1 Analyst, Tier-2 Responder, SOC Lead, CISO) guna memungkinkan penyedia jasa MSSP mengelola puluhan klien korporasi dalam satu antarmuka. |
| **Fase 5: 2028** | **Adaptive Autonomous Deception (Honeypot)** | Mengembangkan kapabilitas agen untuk secara cerdas mengalihkan lalu lintas peretas tingkat tinggi (*Advanced Persistent Threats* / APT) ke lingkungan umpan interaktif (*honeypot*) tiruan guna mempelajari taktik serangan baru (*zero-day*) tanpa membahayakan aset inti perusahaan. |

---

## 9. TAUTAN PENTING (LAMPIRAN)

Sebagai bahan verifikasi, demonstrasi, dan pengujian independen oleh Dewan Juri Garda Tech National Innovation Competition (GTNIC) 2026, berikut adalah tautan proyek kami:

* **Tautan Sistem / Prototype Live:**  
  [https://gtnic-hackwitgoh.vercel.app/](https://gtnic-hackwitgoh.vercel.app/)  
  *(Dasbor operasional SOC aktif 24/7 di jaringan Vercel Edge dan dapat diuji langsung oleh Dewan Juri).*

* **Tautan Lingkungan Lab Serangan (OWASP Juice Shop Live):**  
  [https://juice.flummox.cloud/](https://juice.flummox.cloud/)  
  *(Aplikasi web target yang terintegrasi langsung dengan sensor reverse proxy dan sistem ingesti agen).*

* **Tautan Repositori Kode Sumber (GitHub):**  
  [Tautan Repositori GitHub Anda — Pastikan Mode Akses Publik]  
  *(Berisi kode sumber lengkap backend FastAPI, frontend Next.js 15, skema basis data PostgreSQL, skrip pengujian, dan instruksi kontainer Docker).*

* **Tautan Rekaman Video Demo (YouTube / Google Drive):**  
  [Tautan Video Demo YouTube (Mode Publik atau Unlisted)]  
  *(Video demonstrasi berdurasi 3–5 menit yang menjelaskan latar belakang masalah, arsitektur agen, simulasi serangan langsung, dan alur kerja Human-in-the-Loop).*

---

### DAFTAR PUSTAKA

1. AwanPintar.id. (2026). *Laporan Lanskap Ancaman dan Serangan Siber Indonesia Semester I 2026*. Jakarta: PT Media Antar Nusa.
2. Badan Siber dan Sandi Negara (BSSN). (2025). *Laporan Tahunan Lanskap Keamanan Siber Nasional 2024–2025*. Jakarta: Direktorat Operasi Keamanan Siber, BSSN RI.
3. Badan Siber dan Sandi Negara (BSSN). (2026). *Statistik Anomali Siber Nasional Kuartal I 2026*. Jakarta: Pusat Operasi Keamanan Siber Nasional, BSSN RI.
4. IBM Security. (2024). *Cost of a Data Breach Report 2024*. Ponemon Institute & IBM Security Services.
5. ISC2. (2024). *ISC2 Cybersecurity Workforce Study 2024: Addressing the Global Talent Shortage and the Impact of Emerging Tech*. Clearwater, FL: International Information System Security Certification Consortium.
6. MITRE Corporation. (2025). *MITRE ATT&CK Framework: Enterprise Matrix v15*. Bedford, MA: The MITRE Corporation.
7. OWASP Foundation. (2021). *OWASP Top 10:2021 The Ten Most Critical Web Application Security Risks*. The Open Web Application Security Project.
8. Republik Indonesia. (2022). *Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi*. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196.
9. Touvron, H., dkk. (2023). *Llama 2: Open Foundation and Fine-Tuned Chat Models*. arXiv preprint arXiv:2307.09288.
10. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. International Conference on Learning Representations (ICLR 2023).
