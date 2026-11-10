# GTNIC AI Agent

**Sistem pemantauan dan investigasi ancaman keamanan dengan dashboard SOC, AI Agent, dan bot Discord.**

GTNIC AI Agent membantu tim melihat aktivitas mencurigakan, membaca bukti insiden, dan mencatat keputusan analis dalam satu alur. Proyek ini menggunakan OWASP Juice Shop sebagai aplikasi latihan untuk menguji deteksi serangan web.

## Mulai dari sini

| Kebutuhan | Buka |
| --- | --- |
| Membaca panduan penggunaan, arti fitur, dan langkah demo | [Panduan penggunaan dan pengujian](docs/PANDUAN_PENGGUNAAN.md) |
| Melihat daftar ancaman dan detail insiden | [Dashboard GTNIC](https://gtnic-hackwitgoh.vercel.app/) |
| Membuka aplikasi target latihan | [OWASP Juice Shop — lab tim](https://juice.flummox.cloud/) |
| Menjalankan atau memahami backend | [Dokumentasi backend](backend/README.md) |
| Menjalankan atau memahami frontend | [Dokumentasi frontend](frontend/README.md) |

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
