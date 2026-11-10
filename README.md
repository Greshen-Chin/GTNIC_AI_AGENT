# GTNIC SOAR — Autonomous AI SOC Agent

**Sistem pemantauan, triase otonom, dan investigasi ancaman siber enterprise berbasis Multi-Tool Calling dan Anti-Halusinasi Deterministik.**  
*Diajukan untuk Garda Tech National Innovation Competition (GTNIC) 2026 — Kategori: AI Agent Development.*

GTNIC SOAR mentransformasi operasi Security Operations Center (SOC) enterprise: memangkas waktu investigasi ancaman dari rata-rata ~25 menit menjadi **3–8 detik** (efisiensi 99,5%) melalui loop *tool calling* otonom, verifikasi fakta anti-halusinasi deterministik, matriks bukti *Pro vs Contra*, dan tata kelola *Human-in-the-Loop*.

## 🚀 Tautan Akses Cepat

| Kebutuhan | Tautan / Berkas |
| --- | --- |
| 🌐 **Live SOC Dashboard (Vercel)** | [https://gtnic-hackwitgoh.vercel.app/](https://gtnic-hackwitgoh.vercel.app/) |
| 🎯 **Live Attack Simulation Lab (Juice Shop)** | [https://juice.flummox.cloud/](https://juice.flummox.cloud/) |
| 📄 **Dokumen Proposal Final (Markdown)** | [docs/PROPOSAL_FINAL.md](docs/PROPOSAL_FINAL.md) |
| 📑 **Berkas Word Proposal (Siap Edit/Export PDF)** | [docs/GTNIC2026_Proposal_GTNIC_SOAR.docx](docs/GTNIC2026_Proposal_GTNIC_SOAR.docx) |
| 🎬 **Naskah & Storyboard Video Demo (3-5 Menit)** | [docs/SCRIPT_VIDEO_DEMO.md](docs/SCRIPT_VIDEO_DEMO.md) |
| ✍️ **Surat Pernyataan Keaslian Karya** | [docs/SURAT_PERNYATAAN_KEASLIAN.md](docs/SURAT_PERNYATAAN_KEASLIAN.md) / [.docx](docs/Surat_Pernyataan_Keaslian_Karya.docx) |
| 📊 **Analisis Penilaian & Pemetaan Guide Book** | [docs/ANALISIS.md](docs/ANALISIS.md) |
| 📖 **Panduan Penggunaan & Pengujian Lengkap** | [docs/PANDUAN_PENGGUNAAN.md](docs/PANDUAN_PENGGUNAAN.md) |
| ⚙️ **Dokumentasi Teknis Backend** | [backend/README.md](backend/README.md) |
| 💻 **Dokumentasi Frontend** | [frontend/README.md](frontend/README.md) |

**Dashboard adalah tempat melihat hasil deteksi. Juice Shop adalah tempat melakukan pengujian pada lab yang disediakan tim.** Kita juga memiliki **bot Discord** untuk mengirim pemberitahuan insiden ke channel tim ketika integrasinya aktif dan terkonfigurasi.

## Gambaran alur

```text
Pengujian di OWASP Juice Shop
             |
             v
Reverse proxy Nginx mencatat request
             |
             v
Log forwarder mengirim catatan ke backend
             |
             v
Backend memeriksa pola ancaman dan menyimpan insiden
             |
             +----> Dashboard: daftar insiden, bukti, dan keputusan analis
             |
             +----> Bot Discord: notifikasi insiden
             |
             +----> n8n: workflow tambahan jika dikonfigurasi
```

Selain deteksi pola request Juice Shop, backend menyediakan jalur investigasi AI dengan tool pencarian alert Wazuh dan referensi MITRE/OWASP. Detail yang tersedia pada setiap insiden bergantung pada jalur yang membuatnya.

## Struktur proyek

```text
GTNIC_AI_AGENT/
|-- docs/          Panduan pengguna dan pengujian
|-- frontend/      Dashboard berbasis Next.js dan React
|-- backend/       API FastAPI, deteksi, investigasi, dan integrasi Discord
|-- wazuh/         Berkas integrasi Wazuh
`-- README.md      Pengantar proyek
```

Untuk panduan demo dari awal sampai pemeriksaan hasil, lanjutkan ke [panduan penggunaan](docs/PANDUAN_PENGGUNAAN.md).
