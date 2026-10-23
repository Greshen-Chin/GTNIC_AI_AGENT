# GTNIC SOAR-API 

Layanan **soar-api** berbasis FastAPI yang bertugas sebagai backend tool calling investigasi keamanan, integrasi RAG MITRE & OWASP via **Google Cloud Vertex AI**, serta penyaji data REST API untuk Dashboard SOC.

---

## 🏗️ Peran dan Arsitektur Layanan

Sesuai spesifikasi teknis **Mini-SOAR GTNIC**:
1. **Tool Read-Only untuk AI Agent (`/internal/tools/*`)**:
   - `POST /internal/tools/search_alerts_by_ip`: Query Wazuh Indexer (OpenSearch), jendela 24 jam terakhir, max 20 alert.
   - `POST /internal/tools/get_login_history`: Agregasi rule `100100` (gagal) vs `100103` (berhasil) per IP.
   - `POST /internal/tools/mitre_owasp_rag`: Embed query menggunakan model `text-embedding-004` (768 dimensi) di **Google Cloud Vertex AI**, lalu cosine search top-4 di tabel `security_knowledge` PostgreSQL pgvector.
   - `POST /internal/agent/investigate`: Endpoint autonomous agent pipeline yang mengeksekusi tool calling loop, validasi deterministik, kalkulasi skor keparahan (*severity*) & *confidence*, dan menyimpan insiden ke database.
2. **API Baca untuk Dashboard SOC (`/api/*`)**:
   - `GET /api/incidents`: Antrean tiket insiden.
   - `GET /api/incidents/{id}`: Detail insiden lengkap (Attack Story, Bukti Pro vs Kontra, Tool Trace Audit).
   - `GET /api/stats`: Metrik ringkasan (Total, Critical, High, Active, Mitigated, Rata-rata Confidence).
   - `GET /api/benchmark`: Evaluasi performa 12 skenario lab (Agent vs Baseline).
3. **Endpoint Keputusan Analis (`/api/incidents/{id}/decision`)**:
   - Merekam persetujuan (*Approve*) atau penolakan (*Reject/False Positive*) oleh analis manusia, mencatat `decided_by` dan `decided_at`.

---

## 🔑 Autentikasi & Keamanan

| Endpoint | Header Wajib | Token / Kunci |
|---|---|---|
| `/internal/*` | `X-Internal-Token` atau `Authorization: Bearer <token>` | `INTERNAL_TOKEN` (`d51ebc9c939396154831ec6e856b6a03`) |
| `/api/*` | `X-Dashboard-API-Key` atau `X-API-Key` | `DASHBOARD_API_KEY` (`e8c491f27a6b40d39e8a15b2c7f4019a`) |

---

## ☁️ Konfigurasi Google Cloud Vertex AI (ADC via GCP VM)

Projek ini **tidak menggunakan Google AI Studio**, melainkan **Google Cloud Vertex AI** sehingga kuota dan biaya terpotong langsung dari Google Cloud Project Anda.

Karena backend di-host di Virtual Machine GCP (Google Compute Engine), autentikasi menggunakan **Application Default Credentials (ADC)** secara native via Service Account VM yang memiliki role `roles/aiplatform.user`. File `GOOGLE_APPLICATION_CREDENTIALS` (JSON key) **tidak diperlukan**.

Variabel pada file `backend/.env`:
```env
GOOGLE_CLOUD_PROJECT=project-09be656d-5a5d-473b-a55
GOOGLE_CLOUD_LOCATION=us-central1
LLM_MODEL=gemini-3.8-flash
EMBED_MODEL=text-embedding-004
EMBED_DIM=768
```

> **Catatan Pengujian Offline / Standalone**: Jika dijalankan di laptop lokal tanpa kredensial GCP, sistem secara otomatis mengaktifkan mode *deterministic simulation fallback* sehingga server tetap dapat berjalan dan diuji tanpa error unhandled exception.

---

## 🚀 Cara Menjalankan Layanan

### 1. Menjalankan Langsung dengan Uvicorn (Lokal)
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Dokumentasi OpenAPI Swagger interaktif dapat diakses di:
👉 `http://localhost:8000/docs`

### 2. Menjalankan Stack Lengkap dengan Docker Compose
```bash
cd backend
docker compose -f docker-compose.soar.yml up -d --build
```

### 3. Menjalankan Ingest RAG (Tahap 7)
```bash
python ingest_rag.py
```

### 4. Menjalankan Test Suite
```bash
python -m pytest -v tests/
```
