# Panduan GTNIC AI Agent

**Kenali aplikasinya, lakukan pengujian di lab, lalu periksa hasilnya di dashboard dan Discord.**

[Kembali ke pengantar proyek](../README.md)

## 1. Apa itu GTNIC AI Agent?

GTNIC AI Agent adalah sistem yang membantu tim keamanan memantau aktivitas mencurigakan dan meninjau insiden. Sistem mengumpulkan informasi, menyajikan bukti, dan menyediakan tempat bagi analis untuk mencatat keputusan.

Untuk demo ini, OWASP Juice Shop digunakan sebagai target latihan. Aktivitas yang melewati proxy pemantauan diperiksa oleh backend. Jika cocok dengan pola ancaman yang dikenali, sistem membuat insiden yang dapat dilihat pada dashboard.

Tujuan demo adalah memperlihatkan hubungan antara **aktivitas pengujian → deteksi → bukti insiden → notifikasi → peninjauan analis**.

## 2. Dua website yang digunakan

| Website | Link | Kegunaan |
| --- | --- | --- |
| Dashboard GTNIC | [gtnic-hackwitgoh.vercel.app](https://gtnic-hackwitgoh.vercel.app/) | Melihat ancaman yang terdeteksi, tingkat keparahan, sumber aktivitas, bukti, dan detail insiden. |
| OWASP Juice Shop — lab tim | [juice.flummox.cloud](https://juice.flummox.cloud/) | Aplikasi target untuk mencoba skenario pengujian keamanan dalam lingkungan latihan tim. |

**Cara menggunakannya:** buka kedua link pada tab berbeda. Lakukan pengujian di tab Juice Shop, kemudian pindah ke tab dashboard untuk memeriksa insiden yang terbentuk.

OWASP Juice Shop adalah aplikasi yang sengaja dibuat memiliki celah keamanan untuk pelatihan, demonstrasi, dan pengujian alat keamanan. Penjelasan resminya tersedia di [halaman proyek OWASP Juice Shop](https://owasp.org/projects/juice-shop).

Gunakan target lab yang disediakan sesuai ruang lingkup pengujian tim. Alamat lab di atas adalah deployment tim; ketersediaannya bergantung pada layanan yang sedang berjalan.

## 3. Istilah yang perlu diketahui

| Istilah | Arti sederhana |
| --- | --- |
| Threat / ancaman | Aktivitas atau pola yang berpotensi membahayakan aplikasi. |
| Alert | Peringatan bahwa sistem menemukan aktivitas yang perlu diperiksa. |
| Incident / insiden | Catatan kejadian yang dapat dibuka untuk ditinjau, lengkap dengan informasi pendukung yang tersedia. |
| SOC | Security Operations Center: tim atau fungsi yang memantau keamanan dan menindaklanjuti peringatan. |
| SOAR | Security Orchestration, Automation, and Response: penghubung alat keamanan dan alur penanganan insiden. |
| AI Agent | Komponen yang dapat menjalankan tool investigasi dan membantu menyusun penilaian berdasarkan informasi yang diperoleh. |
| Request | Permintaan dari browser atau alat pengujian kepada server, misalnya pencarian produk atau pengiriman formulir login. |
| Payload | Bagian input yang digunakan dalam pengujian; nilainya dapat tercatat sebagai bukti. |
| Log | Catatan aktivitas aplikasi atau server. |
| Source IP | Alamat IP sumber yang tercatat dalam log; pada jaringan dengan proxy, nilainya bergantung pada konfigurasi pencatatan. |
| Severity | Tingkat keparahan atau prioritas suatu insiden. |
| Confidence | Skor keyakinan penilaian sistem. Angka ini bukan jaminan bahwa serangan berhasil. |
| False positive | Aktivitas yang terdeteksi sebagai ancaman, tetapi setelah ditinjau dinilai bukan ancaman. |
| Mitigasi | Tindakan untuk mengurangi risiko atau dampak ancaman. |

## 4. Mengenal dashboard

### Halaman utama: Incident Queue & Threat Triage

Halaman ini menampilkan antrean insiden dan ringkasan pemantauan. Data diperbarui melalui polling setiap **3 detik** ketika koneksi backend tersedia. Waktu sampai insiden muncul juga dipengaruhi pengiriman log dan pemrosesan backend.

| Elemen tampilan | Cara membacanya |
| --- | --- |
| Active Threat Queue | Jumlah insiden yang masih aktif dan belum diselesaikan melalui keputusan analis. |
| Critical Priority | Jumlah insiden dengan tingkat keparahan Critical. |
| Enforced Mitigations | Jumlah insiden dengan keputusan mitigasi disetujui. Periksa pelaksanaan tindakan pada sistem terkait secara terpisah. |
| Avg Correlation Conf. | Rata-rata skor confidence insiden. |
| Correlation Active | Permintaan data dashboard berjalan tanpa error yang dilaporkan. |
| Backend Offline / Retrying | Dashboard mengalami kendala mengakses API dan akan mencoba kembali. |

Gunakan kolom pencarian untuk mencari berdasarkan judul, IP, aset, atau ID insiden. Filter **Severity**, **Verdict**, dan **Status** membantu mempersempit daftar. Klik salah satu baris untuk membuka detailnya.

### Halaman detail insiden

| Bagian | Isi dan kegunaan |
| --- | --- |
| Identitas insiden | ID, waktu deteksi, judul, sumber IP, dan aset target untuk mencocokkan kejadian dengan pengujian. |
| Severity | Critical, High, Medium, atau Low; membantu menentukan urutan penanganan. |
| Verdict | Malicious, Suspicious, Benign, atau Under Review; menunjukkan penilaian insiden. |
| Attack Story | Urutan kejadian yang tersedia untuk membantu memahami apa yang diamati. |
| Pro Evidence | Bukti yang mendukung dugaan ancaman. |
| Contra Evidence | Bukti yang melemahkan dugaan ancaman, jika tersedia. |
| Tool Trace | Catatan pemanggilan tool investigasi, jika insiden melalui jalur investigasi tersebut. |
| MITRE / OWASP | Konteks referensi keamanan yang tersedia pada insiden. |
| Rekomendasi mitigasi | Saran tindak lanjut, jika disediakan oleh hasil investigasi. |

Insiden dari pemeriksaan log Juice Shop dapat memiliki bukti request dan cerita singkat, sementara tool trace atau konteks MITRE/OWASP masih kosong. Jalur ini memakai deteksi pola, sehingga tidak setiap insiden merupakan hasil investigasi AI.

### Tombol keputusan analis

- **Approve Mitigation:** mencatat persetujuan analis. Dashboard kemudian memetakan insiden menjadi **Mitigated**.
- **Reject (False Positive):** mencatat penolakan dan menampilkan status **False Positive**.

Endpoint keputusan pada backend mencatat keputusan, identitas analis, dan waktu keputusan. Label persetujuan pada dashboard sendiri belum membuktikan bahwa firewall memblokir IP atau bahwa tindakan mitigasi eksternal telah dijalankan.

## 5. Jenis ancaman yang dikenali pada jalur Juice Shop

Backend memeriksa pola pada **URL request** dan **body request**, termasuk input formulir yang diteruskan melalui proxy.

| Jenis | Penjelasan sederhana | Label internal | Severity pada detektor saat ini |
| --- | --- | --- | --- |
| SQL Injection | Input yang menyerupai usaha mengubah perintah query database. | `sql_injection` | High |
| Cross-Site Scripting / XSS | Input yang menyerupai penyisipan skrip ke halaman web. | `cross_site_scripting` | Medium |
| Path Traversal | Input yang menyerupai usaha mengakses direktori atau berkas di luar lokasi yang semestinya. | `path_traversal` | High |
| Command Injection | Input yang menyerupai usaha menyisipkan perintah sistem operasi. | `command_injection` | Critical |

Deteksi ini mencatat **percobaan atau pola mencurigakan**, bukan bukti bahwa celah berhasil dieksploitasi. Jika satu request cocok dengan beberapa pola, implementasi saat ini memilih satu kategori dengan urutan prioritas: Command Injection, SQL Injection, Path Traversal, lalu XSS.

Skor confidence untuk jalur deteksi pola ini saat ini ditetapkan **80%** di kode. Nilai tersebut bukan hasil pengukuran keberhasilan serangan atau penilaian AI per request.

## 6. Cara mencoba demo

### Persiapan

1. Buka [dashboard GTNIC](https://gtnic-hackwitgoh.vercel.app/).
2. Buka [Juice Shop lab tim](https://juice.flummox.cloud/) pada tab lain.
3. Pastikan dashboard tidak menampilkan error koneksi backend.
4. Catat waktu mulai pengujian dan jumlah insiden awal agar hasil baru mudah dikenali.
5. Siapkan channel Discord tim untuk memeriksa notifikasi bot jika integrasinya aktif.

### Percobaan pertama: aktivitas biasa

1. Pada Juice Shop, buka katalog dan cari produk dengan kata biasa, misalnya `apple`.
2. Kembali ke dashboard dan amati antrean insiden.
3. Catat apakah aktivitas tersebut memunculkan insiden baru. Aktivitas biasa tanpa pola yang dikenali semestinya tidak memicu detektor pola ini.

### Percobaan kedua: pola SQL Injection

1. Pada kolom pencarian produk Juice Shop, masukkan contoh input lab berikut satu kali:

   ```text
   ' OR 1=1 --
   ```

2. Jalankan pencarian sehingga browser mengirim request ke server.
3. Kembali ke dashboard dan tunggu beberapa siklus pembaruan.
4. Cari insiden baru dengan judul yang memuat **Juice Shop SQL injection attempt**.
5. Buka detailnya dan periksa waktu, target `juice-shop`, source IP, serta bukti request.
6. Periksa apakah bot Discord mengirim pemberitahuan untuk ID insiden yang sama.

**Hasil yang diharapkan:** jika request melewati proxy yang dipantau dan seluruh layanan terhubung, sistem mencatat insiden SQL Injection dengan severity High. Respons pencarian Juice Shop dapat berbeda; indikator keberhasilan demo pemantauan adalah kecocokan request uji dengan bukti insiden.

### Skenario tambahan

| Skenario | Yang diperiksa |
| --- | --- |
| XSS pada challenge lab yang sesuai | Apakah pola skrip pada request server tercatat sebagai `cross_site_scripting`. |
| Path Traversal pada skenario lab yang sesuai | Apakah pola jalur berkas pada request tercatat sebagai `path_traversal`. |
| Command Injection pada skenario lab yang sesuai | Apakah pola perintah pada request tercatat sebagai `command_injection`. |
| Peninjauan analis | Apakah keputusan Approve atau Reject tersimpan dan status dashboard berubah sesuai pilihan. |

Gunakan petunjuk challenge Juice Shop untuk skenario tambahan. Perubahan yang hanya terjadi di browser, termasuk pada fragmen URL setelah `#`, tidak otomatis masuk ke log request server.

## 7. Bot Discord

**Kita juga memiliki bot Discord untuk notifikasi insiden keamanan.** Ketika insiden baru tersimpan, backend memicu pengiriman pesan ke channel Discord yang dikonfigurasi. Tim dapat memantau peringatan dari Discord lalu membuka dashboard untuk pemeriksaan lebih lengkap.

Pesan bot memuat informasi yang tersedia, antara lain:

- Judul dan jenis ancaman.
- Source IP serta lokasi pola, misalnya URL atau Request Body.
- Severity, skor confidence, dan verdict.
- ID insiden untuk dicocokkan dengan dashboard.
- Cuplikan payload atau bukti, serta ringkasan kejadian jika tersedia.

Bagi pengelola, pengiriman memerlukan konfigurasi backend berikut:

```dotenv
DISCORD_ENABLED=true
DISCORD_BOT_TOKEN=<token-bot-milik-tim>
DISCORD_CHANNEL_ID=<id-channel-notifikasi>
```

Bot harus memiliki akses untuk mengirim pesan dan embed pada channel tujuan. Simpan token di konfigurasi server. Link undangan Discord belum dicantumkan karena belum diberikan.

Jika pengiriman Discord gagal, insiden yang sudah tersimpan tetap dapat diperiksa di dashboard. Implementasi saat ini menyediakan notifikasi insiden; panduan ini tidak mengasumsikan adanya perintah chat atau kontrol mitigasi melalui Discord.

## 8. Jika hasil belum muncul

| Kondisi | Pemeriksaan yang disarankan |
| --- | --- |
| Website tidak bisa dibuka | Periksa alamat, koneksi, dan status deployment bersama pengelola lab. |
| Dashboard menampilkan Backend Offline | Periksa layanan backend, konfigurasi koneksi frontend, dan autentikasi API. |
| Request uji belum menghasilkan insiden | Pastikan request benar-benar dikirim ke server melalui proxy pemantauan; periksa log Nginx dan layanan log forwarder. |
| Insiden sulit ditemukan | Kosongkan filter, lalu cari berdasarkan judul, IP, atau waktu pengujian. |
| Dashboard menerima insiden, Discord tidak | Periksa pengaktifan bot, token, channel ID, izin channel, dan log pengiriman backend. |
| Tool Trace atau referensi kosong | Periksa asal insiden; deteksi pola Juice Shop tidak otomatis menjalankan seluruh tool investigasi AI. |

## 9. Checklist pencatatan demo

- [ ] Kedua website dapat diakses.
- [ ] Dashboard terhubung ke backend.
- [ ] Waktu dan kondisi awal dicatat.
- [ ] Aktivitas biasa dicoba sebagai pembanding.
- [ ] Request pengujian dikirim melalui lab Juice Shop.
- [ ] Insiden yang sesuai ditemukan dan buktinya diperiksa.
- [ ] Status pengiriman notifikasi Discord dicatat.
- [ ] Keputusan analis dicatat jika tahap peninjauan dilakukan.

Checklist ini adalah panduan pelaksanaan, bukan laporan pengujian yang sudah dijalankan. Status deployment dan pengiriman Discord perlu dibuktikan pada sesi demo.

## 10. Hasil Pengujian dan Bukti Demo

<!-- Sengaja dikosongkan untuk diisi kemudian: hasil pengujian, screenshot dashboard, dan notifikasi Discord. -->

<br>
<br>
<br>
<br>
<br>
