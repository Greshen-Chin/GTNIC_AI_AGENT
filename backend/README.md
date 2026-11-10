# GTNIC SOAR-API 

## Perbaikan investigasi berulang pada log Juice Shop

Penyebab yang dikonfirmasi dari API dashboard: insiden berulang memiliki waktu
log yang sama (`2026-11-10T14:31:48+00:00`), URL `/etc/passwd`, dan status HTTP
`304`, sedangkan investigasi membutuhkan sekitar 19–322 detik. Forwarder sebelumnya
memakai timeout 5 detik, sehingga mengirim ulang satu log sebelum investigasinya
selesai. Nilai `dedup_key` sebelumnya disimpan tanpa pemeriksaan duplikat.

Perbaikan KISS:

- Forwarder menunggu respons investigasi tanpa batas waktu baca 5 detik; timeout
  koneksi dan pengiriman tetap 5 detik.
- Setiap baris log mendapatkan `event_id` stabil dari identitas file, posisi baca,
  dan isi baris. Retry dan restart forwarder mempertahankan identitas tersebut.
- Backend memeriksa identitas event di database sebelum menjalankan AI. Log yang
  sudah diproses mengembalikan ID insiden yang sama tanpa investigasi atau
  notifikasi ulang. Forwarder lama yang belum mengirim `event_id` menggunakan
  fingerprint isi event bertimestamp sebagai kompatibilitas sementara.
- Pemrosesan ingest diserialkan pada API satu worker agar retry bersamaan tidak
  memulai dua investigasi. Request baru dari IP yang sama tetap diperiksa.

Jalankan tes regresi dari direktori `backend`:

```powershell
python -m pytest tests/test_ingest_retries.py -q
```

Untuk menerapkan kode baru di server, build ulang **kedua** layanan dari direktori
`backend` pada checkout yang sudah berisi perbaikan:

```bash
docker compose -f docker-compose.soar.yml up -d --build soar-api juice-log-forwarder
```

Perbaikan ini tidak menghapus catatan insiden lama. Dengan PostgreSQL tersedia,
pemeriksaan duplikat tetap bekerja setelah restart API. Fallback in-memory hanya
menyimpan identitas selama proses hidup. Mekanisme lock mengikuti konfigurasi
deployment saat ini (`uvicorn --workers 1`); deployment multiworker membutuhkan
koordinasi deduplikasi di database sebelum investigasi.

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

## Juice Shop attack monitoring

Juice Shop is published through the Nginx reverse proxy on `http://localhost:3000`.
The proxy writes JSON access logs (including request URI and buffered request body)
to a shared Docker volume; `juice-log-forwarder` ships those entries to the authenticated
SOAR endpoint. The API detects SQLi/XSS patterns in both the request URI and POST request body,
stores a pending incident in PostgreSQL, and posts a `security.alert` event to n8n when
`WEBHOOK_URL` is configured. The existing dashboard polls the incident API every three seconds,
so the incident appears in the queue automatically.

Add the active n8n **Production URL** to `backend/.env`:

```env
WEBHOOK_URL=http://soar-n8n:5678/webhook/your-active-workflow-path
```

The n8n workflow should start with a **Webhook** node using that path, then route
`security.alert` to the team's chosen channel or ticketing system. The incoming
JSON includes `incident_id`, `threat_type`, `severity`, `source_ip`, `payload`,
and `dashboard_url`. Keep the workflow active so n8n's production webhook accepts
events.

Recreate the stack after changing the Compose file or `.env`:

```powershell
docker compose -f docker-compose.soar.yml up -d --build
```

Attack test: open `http://localhost:3000` through the proxy and send a SQLi probe
either in a URL query (e.g. `/rest/products/search?q=%27%20OR%201%3D1%20--%20`) or directly
via the login form POST body (`' OR 1= 1--`). Then check `GET /api/incidents` in the dashboard
or the backend logs. Only traffic sent through port 3000 is monitored; direct access to the Juice
Shop container is not exposed by this Compose file. The detector inspects both request URLs
and POST bodies, and reports suspicious attempts rather than proving exploitation.

### 3. Menjalankan Ingest RAG (Tahap 7)
```bash
python ingest_rag.py
```

### 4. Menjalankan Test Suite
```bash
python -m pytest -v tests/
```
