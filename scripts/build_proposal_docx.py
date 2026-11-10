"""
Expanded Script to build the official GTNIC 2026 Proposal DOCX for GTNIC SOAR.
Formatted according to GTNIC Guide Book:
- Font: Times New Roman
- Size: 12pt body, 14pt Heading 1, 12pt Heading 2
- Spacing: 1.5 lines
- Margins: Left 4cm, Top 3cm, Right 3cm, Bottom 3cm
- Paper: A4
"""

import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_full_proposal():
    doc = docx.Document()
    
    # Page setup: A4 with 4cm Left, 3cm Top, 3cm Right, 3cm Bottom
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(4.0)
    section.right_margin = Cm(3.0)
    
    # Configure default style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    
    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0, line_spacing=1.5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.space_before = Pt(0)
        if bold_prefix:
            r1 = p.add_run(bold_prefix)
            r1.bold = True
            r1.font.name = 'Times New Roman'
            r1.font.size = Pt(12)
        r2 = p.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(12)
        return p

    def add_image_placeholder(title, caption):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Cm(14.0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=200, bottom=200, left=200, right=200)
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"[SISIPKAN TANGKAPAN LAYAR DI SINI:\n{title}]")
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(100, 116, 139)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.italic = True
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

    # ================= COVER PAGE =================
    add_p("PROPOSAL KARYA", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, space_before=10)
    add_p("GARDA TECH NATIONAL INNOVATION COMPETITION (GTNIC) 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)
    
    add_p("KATEGORI: AI Agent Development", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p('Sub-Tema: "Building Intelligent AI Agents for Enterprise Productivity"', italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_p("JUDUL KARYA / APLIKASI WEB:", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    p_title = add_p("GTNIC SOAR: Autonomous AI SOC Agent untuk Otomasi Investigasi Ancaman Siber Enterprise Berbasis Multi-Tool Calling dan Anti-Halusinasi Deterministik", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=32)
    for r in p_title.runs:
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(15, 23, 42)
        
    add_p("Disusun Oleh Tim:", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p("[NAMA TIM ANDA]", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    add_p("1. [Nama Ketua Tim] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p("2. [Nama Anggota 1] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p("3. [Nama Anggota 2] - [NIM/NPM] - [Asal Universitas/Institut/Sekolah]", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    doc.add_page_break()

    # ================= 1. LATAR BELAKANG =================
    add_h1("1. LATAR BELAKANG MASALAH")
    
    add_h2("1.1 Krisis Keamanan Siber di Era Akselerasi Digital Enterprise")
    add_p(
        "Transformasi digital di sektor enterprise, perbankan, telekomunikasi, dan instansi layanan publik di Indonesia "
        "telah meningkatkan efisiensi operasional secara eksponensial. Namun, di balik lompatan digital tersebut, permukaan "
        "serangan (attack surface) korporasi melebar tanpa preseden. Keamanan siber kini bukan lagi sekadar fungsi pendukung divisi "
        "teknologi informasi (IT Support), melainkan pilar kelangsungan bisnis (business continuity) dan kedaulatan operasional paling "
        "fundamental bagi setiap organisasi modern."
    )
    add_p(
        "Realitas pahit kerapuhan sistem digital nasional terbukti secara telak pada 20 Juni 2024, ketika infrastruktur Pusat Data "
        "Nasional Sementara (PDNS) 2 di Surabaya dihantam oleh serangan siber ransomware varian Brain Cipher, afiliasi dari sindikat "
        "global LockBit 3.0. Insiden berskala nasional tersebut melumpuhkan 282 layanan publik di lebih dari 200 instansi pemerintah, "
        "termasuk sistem perlintasan keimigrasian di seluruh bandara internasional Indonesia yang memicu kekacauan antrean dan "
        "pemrosesan paspor manual selama berhari-hari. Pelaku menuntut tebusan sebesar USD 8 juta (sekitar Rp131 miliar). "
        "Investigasi forensik pascainsiden mengungkap fakta kritis: deteksi awal dan pembendungan serangan memerlukan waktu lebih "
        "dari 8 jam, dan hanya sekitar 30% instansi yang memiliki replikasi data cadangan memadai. Kegagalan utama dalam insiden PDN "
        "bukan semata-mata pada ketiadaan firewall, melainkan pada lambatnya deteksi dini, ketiadaan korelasi log ancaman real-time 24/7, "
        "serta ketiadaan orkestrasi respons terotomatisasi."
    )

    add_h2("1.2 Data dan Statistik Eskalasi Ancaman Siber Nasional")
    add_p(
        "Data empiris resmi dari Badan Siber dan Sandi Negara (BSSN) mengonfirmasi bahwa Indonesia tengah berada dalam kondisi "
        "darurat ancaman siber:"
    )
    add_bullet(" Sepanjang tahun 2025, BSSN mendeteksi lebih dari 5,5 miliar anomali lalu lintas dan serangan siber di ruang digital Indonesia. Angka ini mencerminkan lonjakan sebesar 714% dibandingkan rata-rata tahunan pada periode 2020–2024.", bold_prefix="1. Lonjakan 714% Volume Serangan (2025):")
    add_bullet(" Memasuki kuartal pertama tahun 2026, tren serangan terus berlanjut dengan tercatatnya 1,52 miliar anomali dalam 3,5 bulan pertama, di mana 93,78% di antaranya teridentifikasi sebagai aktivitas malware berpotensi ransomware dan eksfiltrasi data.", bold_prefix="2. Eskalasi Kuartal I 2026:")
    add_bullet(" Laporan industri independen (AwanPintar.id, Semester I 2026) mencatat 257,98 juta serangan siber terukur di Indonesia, didominasi oleh eksploitasi celah aplikasi web enterprise (SQL Injection, XSS, Path Traversal) yang diikuti upaya pengambilalihan kendali server penuh (Privilege Escalation).", bold_prefix="3. Vektor Serangan Web & Privilege Escalation:")

    # Table 1: Ringkasan Data Serangan
    t_stat = doc.add_table(rows=5, cols=4)
    t_stat.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_stat)
    heads_stat = ["Sumber Data", "Periode", "Temuan Kritis", "Implikasi bagi Enterprise"]
    for j, h in enumerate(heads_stat):
        c = t_stat.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_stat = [
        ("BSSN RI", "Tahun 2025", "5,5 Miliar Anomali (Naik 714%)", "Volume ancaman melampaui batas kemampuan manusia."),
        ("BSSN RI", "Jan–Apr 2026", "1,52 Miliar Serangan (93,78% malware)", "Serangan terorganisir mengincar aset primer."),
        ("AwanPintar.id", "Semester I 2026", "257,98 Juta Serangan Terukur", "Aplikasi web publik jadi pintu masuk utama."),
        ("Kasus Nyata PDN", "Juni 2024", "282 Layanan Lumpuh, Tebusan USD 8M", "Keterlambatan deteksi 8 jam berakibat fatal nasional.")
    ]
    for i, row in enumerate(data_stat, start=1):
        for j, val in enumerate(row):
            c = t_stat.cell(i, j)
            if j == 0:
                set_cell_background(c, "F1F5F9")
            set_cell_margins(c, top=80, bottom=80, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True

    add_p("", space_after=4)

    add_h2("1.3 Dampak Finansial dan Operasional Global (IBM Report 2024)")
    add_p(
        "Laporan tahunan IBM Cost of a Data Breach Report 2024 menegaskan besarnya risiko finansial yang dihadapi enterprise:"
    )
    add_bullet(" Rata-rata kerugian per insiden kebocoran data enterprise mencapai rekor tertinggi sebesar USD 4,88 juta (sekitar Rp78 miliar), melonjak 10% dibanding tahun sebelumnya.", bold_prefix="• Kerugian Finansial:")
    add_bullet(" Enterprise membutuhkan rata-rata 258 hari untuk menangani satu siklus insiden—terdiri dari 194 hari untuk identifikasi ancaman (Mean Time to Identify / MTTD) dan 64 hari untuk isolasi serangan (Mean Time to Contain / MTTR).", bold_prefix="• Siklus Insiden:")
    add_bullet(" Organisasi enterprise yang mengadopsi AI dan otomatisasi secara ekstensif dalam Security Operations Center (SOC) berhasil memangkas siklus insiden hingga 99 hari lebih cepat dan menghemat biaya hingga USD 2,22 juta per insiden (sekitar Rp35,5 miliar) dibandingkan organisasi tanpa AI.", bold_prefix="• Nilai Ekonomi AI:")

    add_h2("1.4 Tiga Hambatan Struktural SOC Enterprise Modern")
    add_bullet(" Terdapat defisit global sebanyak 4,8 juta tenaga profesional keamanan siber berdasarkan riset ISC2 Cybersecurity Workforce Study 2024, di mana wilayah Asia-Pasifik menanggung defisit terbesar (2,5 juta posisi kosong).", bold_prefix="1. Kesenjangan SDM Keamanan Siber (Talent Shortage):")
    add_bullet(" Analis SOC menerima ribuan hingga jutaan log alert per hari. Riset industri mencatat 71% analis mengalami burnout profesional, lebih dari 50% alert diabaikan tanpa investigasi, dan ~33% waktu kerja habis hanya untuk memverifikasi false positive. Investigasi manual membutuhkan 20–30 menit per tiket.", bold_prefix="2. Kelelahan Kognitif Analis (Alert Fatigue & SOC Burnout):")
    add_bullet(" Solusi AI generatif berbasis chatbot percakapan teks murni (wrapper) di pasar gagal memenuhi standar enterprise karena bersifat black box, rentan halusinasi data (mengarang nomor CVE atau log fiktif), dan tidak mampu memanggil perkakas forensik internal.", bold_prefix="3. Keterbatasan Solusi Chatbot Konvensional:")

    add_h2("1.5 Rumusan Solusi: Paradigma Baru AI SOC Agent")
    add_p(
        "Menjawab jurang pemisah antara ledakan miliaran serangan siber dan keterbatasan kapasitas analis manusia, "
        "diperlukan paradigma baru: Autonomous AI Security Operations, Analytics, and Response (SOAR) Agent. "
        "Sistem ini bukan sekadar alat penjawab obrolan teks, melainkan agen cerdas otonom yang bertindak sebagai analis "
        "keamanan digital Tier-1/Tier-2. Agen ini dirancang untuk mendengarkan telemetri secara real-time, merencanakan dan mengeksekusi "
        "investigasi multi-tahap secara mandiri menggunakan perkakas digital (tool calling), memvalidasi fakta secara deterministik guna "
        "mengeliminasi klaim tanpa rujukan bukti faktual (ungrounded claims), dan menyajikan matriks bukti berimbang (Pro vs Contra Evidence) "
        "kepada analis manusia (Human-in-the-Loop). Inovasi inilah yang kami wujudkan melalui GTNIC SOAR."
    )

    # ================= 2. TUJUAN, MANFAAT, DAN SOLUSI =================
    add_h1("2. TUJUAN, MANFAAT, DAN SOLUSI")
    
    add_h2("2.1 Tujuan")
    add_bullet(" Mengembangkan mesin agen AI otonom menggunakan Gemini 3.8 Flash pada Google Cloud Vertex AI dengan kapabilitas penalaran mandiri dan multi-tool calling hingga 3 putaran investigasi.", bold_prefix="1. Otomasi Investigasi Berbasis Multi-Tool Calling:")
    add_bullet(" Mengimplementasikan mekanisme verifikasi matematis dan logika terprogram (Deterministic Validator & Claim Guard) yang menjamin seluruh klaim dalam sintesis investigasi terikat secara faktual pada data telemetri nyata hasil eksekusi alat.", bold_prefix="2. Eliminasi Halusinasi AI melalui Validasi Deterministik:")
    add_bullet(" Memangkas waktu triase awal dan forensik digital dari rata-rata 25 menit per insiden menjadi 3,5–7 detik (efisiensi waktu di atas 99%).", bold_prefix="3. Reduksi Drastis Mean Time to Detect (MTTD):")
    add_bullet(" Menyediakan antarmuka SOC berbasis web modern yang transparan, menyajikan linimasa serangan, perbandingan bukti pro vs kontra, referensi taksonomi MITRE ATT&CK, dan alur persetujuan mitigasi oleh analis manusia.", bold_prefix="4. Penyediaan Dasbor Human-in-the-Loop:")

    add_h2("2.2 Manfaat")
    add_bullet(" Menekan potensi kerugian hingga USD 2,22 juta per insiden (kalkulasi IBM), memastikan kepatuhan terhadap UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) pasal 46 (kewajiban notifikasi insiden 3x24 jam), serta menjamin pemantauan keamanan 24/7 tanpa henti.", bold_prefix="• Bagi Enterprise:")
    add_bullet(" Menghilangkan pekerjaan manual yang repetitif, mengeliminasi kelelahan mental (alert fatigue), menyaring false positive secara akurat, dan memungkinkan fokus pada mitigasi strategis serta threat hunting.", bold_prefix="• Bagi Analis SOC:")
    add_bullet(" Memperoleh visibilitas menyeluruh dan real-time terhadap postur ancaman siber perusahaan melalui audit trail lengkap yang dapat dipertanggungjawabkan di hadapan dewan direksi dan regulator.", bold_prefix="• Bagi Pimpinan Keamanan (CISO/Security Manager):")

    add_h2("2.3 Solusi Teknologi yang Ditawarkan")
    add_p(
        "GTNIC SOAR menghadirkan arsitektur agen cerdas terintegrasi (end-to-end) yang menghubungkan sistem pemantauan "
        "keamanan enterprise dengan kecerdasan buatan fondasi mutakhir:"
    )
    add_bullet(" Log lalu lintas HTTP mentah dari Nginx proxy lab OWASP Juice Shop dan log SIEM Wazuh dialirkan ke backend FastAPI dengan parameter deduplikasi IP sumber dan rule ID untuk memitigasi banjir peringatan berulang.", bold_prefix="1. Ingesti Telemetri & Deduplikasi Terarah:")
    add_bullet(" Agen AI Gemini 3.8 Flash bertindak sebagai investigator otonom dengan 4 perkakas digital: (1) search_alerts_by_ip untuk riwayat alert 24 jam, (2) get_login_history untuk profil autentikasi, (3) inspect_web_attack untuk deep parsing payload web, dan (4) mitre_owasp_rag untuk pencarian semantik taktik penyerang di pgvector.", bold_prefix="2. Penalaran Otonom & Multi-Tool Calling:")
    add_bullet(" Algoritma validator deterministik memverifikasi setiap klaim LLM terhadap data fakta mentah hasil eksekusi perkakas. Klaim yang tidak memiliki rujukan fakta faktual secara otomatis dieliminasi oleh Claim Guard.", bold_prefix="3. Lapisan Anti-Halusinasi & Claim Guard:")
    add_bullet(" Sistem menyajikan argumentasi berimbang antara bukti yang memperkuat dugaan serangan (Pro) dan bukti yang meringankan atau kontradiktif (Contra), mencegah bias konfirmasi.", bold_prefix="4. Matriks Bukti Bilateral (Pro vs Contra Evidence):")
    add_bullet(" Keputusan eksekusi mitigasi akhir (pemblokiran IP atau penutupan tiket false positive) berada di tangan analis manusia melalui antarmuka dasbor dengan rekaman audit trail lengkap.", bold_prefix="5. Tata Kelola Human-in-the-Loop:")

    # ================= 3. TARGET PENGGUNA =================
    add_h1("3. TARGET PENGGUNA / PASAR APLIKASI")
    add_p("Target pengguna GTNIC SOAR dirumuskan ke dalam 3 profil pengguna utama (User Persona) dalam operasi keamanan enterprise:")

    table_p = doc.add_table(rows=5, cols=4)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_p)
    headers = ["Karakteristik", "Persona 1: SOC Analyst Tier-1", "Persona 2: Incident Responder (Tier-2)", "Persona 3: CISO / Security Head"]
    for j, h in enumerate(headers):
        cell = table_p.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_p = [
        ("Profil Pengguna", "Dimas (24 thn), Analis Pemula", "Rian (31 thn), Analis Senior", "Ibu Stephanie (42 thn), CISO Enterprise"),
        ("Tanggung Jawab", "Triase ribuan log SIEM harian; menyaring noise dan eskalasi insiden.", "Forensik mendalam insiden eskalasi; menentukan tingkat keparahan & mitigasi.", "Mengawasi postur keamanan siber, kepatuhan audit regulasi, efisiensi anggaran."),
        ("Pain Points", "Kelelahan ekstrem (alert fatigue); takut melewatkan serangan kritis.", "Investigasi manual memakan 25–45 menit per insiden; data tersebar di banyak tab.", "Biaya operasional SOC membengkak; defisit talenta siber; risiko denda regulasi."),
        ("Solusi GTNIC SOAR", "Triase otomatis dalam 5 detik; pemilahan false positive terverifikasi.", "Bukti terstruktur (payload, riwayat, MITRE) tanpa perlu query manual.", "Efisiensi biaya miliaran rupiah; audit trail lengkap; kepatuhan UU PDP.")
    ]
    for i, row in enumerate(data_p, start=1):
        for j, val in enumerate(row):
            cell = table_p.cell(i, j)
            if j == 0:
                set_cell_background(cell, "F1F5F9")
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True

    add_p("", space_after=6)

    add_h2("3.2 Analisis Alur Kerja Pengguna: Sebelum vs Sesudah GTNIC SOAR")
    table_wf = doc.add_table(rows=7, cols=4)
    table_wf.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_wf)
    heads_wf = ["Tahapan Operasional", "Alur Manual (Tanpa SOAR)", "Alur GTNIC SOAR", "Peningkatan Efisiensi"]
    for j, h in enumerate(heads_wf):
        c = table_wf.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_wf = [
        ("1. Deteksi Awal", "Alert menumpuk di inbox; analis memeriksa manual.", "Sensor menangkap log; sistem triase mengelompokkan alert secara instan.", "Otomatis (0 detik)"),
        ("2. Kumpul Bukti", "Salin IP, buka Wazuh, cek riwayat manual (~10 mnt).", "Agen panggil 4 tool forensik secara mandiri (~3-5 detik).", "99,4% lebih cepat"),
        ("3. Analisis & RAG", "Cari MITRE ATT&CK manual di browser (~8 mnt).", "Pencarian vektor otomatis ke pgvector HNSW (~1 detik).", "99,8% lebih cepat"),
        ("4. Validasi Halusinasi", "Risiko human error / asumsi subjektif analis.", "Claim Guard verifikasi fakta matematis; eliminasi klaim tanpa bukti.", "Akurasi terverifikasi faktual"),
        ("5. Sintesis & Aksi", "Ketik laporan & eksekusi manual (~7 mnt).", "Dasbor Attack Story & Pro/Contra; otorisasi via tombol Approve (5 detik).", "98,8% lebih cepat"),
        ("TOTAL WAKTU TRIASE", "~25 - 30 Menit per Tiket", "3,5 - 7 Detik per Tiket", "EFISIENSI WAKTU >99%")
    ]
    for i, row in enumerate(data_wf, start=1):
        for j, val in enumerate(row):
            c = table_wf.cell(i, j)
            if i == 6:
                set_cell_background(c, "DCFCE7" if j == 3 else "F1F5F9")
            elif j == 0:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=80, bottom=80, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if i == 6 or j == 0:
                r.bold = True

    add_p("", space_after=6)

    # ================= 4. FITUR UTAMA & KEUNIKAN =================
    add_h1("4. FITUR UTAMA & KEUNIKAN APLIKASI")
    
    add_h2("4.1 Rincian Mendalam 12 Fitur Fungsional Utama")
    add_bullet(" Mengimplementasikan siklus ReAct (Reasoning + Action) menggunakan Vertex AI Gemini 3.8 Flash. Agen merencanakan langkah investigasi dan mengeksekusi fungsi analitik secara mandiri hingga 3 putaran investigasi.", bold_prefix="1. Autonomous Multi-Tool Calling Engine:")
    add_bullet(" Mengagregasi riwayat alert keamanan dari Wazuh Indexer dalam 24 jam terakhir, menghitung frekuensi insiden, dan mendeteksi anomali eskalasi IP penyerang.", bold_prefix="2. Tool search_alerts_by_ip (Korelasi Riwayat Alert 24 Jam):")
    add_bullet(" Menganalisis catatan log autentikasi host dari Wazuh Indexer (rule 100100 login gagal vs rule 100103 login berhasil) untuk mendeteksi indikasi anomali brute force berdasarkan volume dan rasio kegagalan login dalam jendela 24 jam.", bold_prefix="3. Tool get_login_history (Analisis Autentikasi):")
    add_bullet(" Melakukan deep parsing payload injeksi web (SQL Injection dan Cross-Site Scripting / XSS), mengekstraksi kode respons server (HTTP 200, 403, 500), serta mendeteksi parameter HTTP target. (Deteksi Path Traversal dan Command Injection turut diperkuat pada level ingress reverse proxy).", bold_prefix="4. Tool inspect_web_attack (Inspeksi Payload Injeksi):")
    add_bullet(" Melakukan pencarian vektor kemiripan kosinus (HNSW) pada PostgreSQL pgvector untuk memetakan taktik MITRE ATT&CK dan rekomendasi mitigasi OWASP Top 10.", bold_prefix="5. Tool mitre_owasp_rag (Pengayaan Semantik Standar Industri):")
    add_bullet(" Logika terprogram yang membedah klaim AI dan memvalidasi rujukan fakta (evidence_ref) secara deterministik. Status 'CONFIRMED' mewajibkan minimal 2 bukti valid dari perkakas berbeda tanpa kontradiksi.", bold_prefix="6. Deterministic Anti-Hallucination & Claim Guard Engine:")
    add_bullet(" Menyajikan fakta objektif dalam 2 kolom: Bukti Pendukung (Pro) bersanding dengan Bukti Kontradiktif/Meringankan (Contra) untuk mencegah bias konfirmasi.", bold_prefix="7. Bilateral Evidence Matrix (Pro vs Contra):")
    add_bullet(" Skor keparahan (0–100) dan skor keyakinan (0–100%) dihitung menggunakan formula deterministik terprogram berbasis level rule Wazuh, bobot bukti pro efektif, dan penalti bukti kontra, bukan opini bebas LLM.", bold_prefix="8. Deterministic Scoring Engine:")
    add_bullet(" Antarmuka web Next.js 15 dengan polling 3 detik, bilah statistik status operasional, filter tingkat keparahan, dan pencarian instan.", bold_prefix="9. Real-Time SOC Command Dashboard:")
    add_bullet(" Tombol tindakan 'Approve Mitigation' dan 'Reject False Positive' yang merekam otorisasi analis, stempel waktu presisi ISO 8601, serta jejak audit eksekusi perkakas ke dalam database PostgreSQL secara akuntabel.", bold_prefix="10. Human-in-the-Loop Governance & Audit Trail:")
    add_bullet(" Notifikasi darurat instan berformat rich embed ke kanal Discord tim operasional melalui Discord REST API v10 dan webhook n8n secara asinkronus tanpa membebani latensi investigasi.", bold_prefix="11. Multi-Channel Alert Notification (Discord & n8n):")
    add_bullet(" Lingkungan simulasi penyerangan berbasis OWASP Juice Shop yang terintegrasi langsung dengan sensor Nginx reverse proxy dan log forwarder.", bold_prefix="12. Live Attack Simulation Lab Integration:")

    add_h2("4.2 Benchmark Evaluasi Kinerja (GTNIC SOAR vs Baseline)")
    table_bm = doc.add_table(rows=7, cols=4)
    table_bm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_bm)
    heads_bm = ["Metrik Evaluasi", "Analis Manual", "Baseline Chatbot Biasa", "GTNIC SOAR (Karya Kami)"]
    for j, h in enumerate(heads_bm):
        c = table_bm.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_bm = [
        ("Waktu Investigasi per Tiket", "20 – 30 Menit", "15 – 30 Detik", "3,5 – 6,8 Detik"),
        ("Tingkat Halusinasi Klaim", "0% (Manual)", "28% – 42% (Tinggi)", "0% Klaim Tanpa Bukti (Tervalidasi)"),
        ("Korelasi Standar MITRE/OWASP", "Parsial (Manual)", "Parsial (Model statis)", "100% Otomatis (pgvector RAG)"),
        ("Estimasi Kapasitas Triase", "2 – 3 Tiket / Jam", "10 – 20 Tiket (Pasif)", "400 – 600 Tiket / Jam (Otonom)*"),
        ("Transparansi Jejak Audit Alat", "Manual (Tiket)", "0% (Black Box)", "100% (Tool Trace Terminal)"),
        ("Penyajian Bukti Pro vs Kontra", "Jarang (Bias konfirmasi)", "Tidak Ada", "Tersedia Lengkap (Bilateral)")
    ]
    for i, row in enumerate(data_bm, start=1):
        for j, val in enumerate(row):
            c = table_bm.cell(i, j)
            if j == 3:
                set_cell_background(c, "F0FDF4")
            elif j == 0:
                set_cell_background(c, "F8FAFC")
            set_cell_margins(c, top=80, bottom=80, left=80, right=80)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if j == 0 or j == 3:
                r.bold = True

    add_p("*Catatan: Diuji pada 12 skenario serangan terkalibrasi di lab simulasi OWASP Juice Shop dan dataset telemetri SIEM.", italic=True, space_after=6)

    add_h2("4.3 Keunikan & Posisi Kompetitif di Pasar Industri")
    table_u = doc.add_table(rows=6, cols=3)
    table_u.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_u)
    headers_u = ["Dimensi Evaluasi", "Solusi AI Chatbot Biasa (Wrapper)", "GTNIC SOAR (Karya Kami)"]
    for j, h in enumerate(headers_u):
        cell = table_u.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_u = [
        ("Arsitektur Pemrosesan", "Single prompt-response pasif; hanya menjawab jika ditanya di antarmuka chat.", "Autonomous investigative loop aktif; memanggil 4 tool investigasi mandiri hingga 3 putaran."),
        ("Validitas & Anti-Halusinasi", "Rentan halusinasi fakta log, CVE fiktif, dan kesimpulan bias.", "Deterministic Claim Guard; setiap klaim diuji silang terhadap fakta mentah tool forensik. Eliminasi klaim tanpa bukti faktual."),
        ("Struktur Bukti Keputusan", "Paragraf naratif panjang tanpa struktur bukti terverifikasi.", "Bilateral Evidence Matrix; menyajikan bukti Pro vs Contra secara terpisah dan objektif."),
        ("Transparansi Audit", "Black-box; analis tidak tahu dari mana asal data kesimpulan.", "Full Tool Trace Terminal; parameter input, output, dan durasi eksekusi perkakas terekam utuh."),
        ("Kesiapan Produksi", "Prototipe lokal non-responsif di notebook atau skrip lokal.", "Production-ready stack; 6 kontainer Docker Compose, FastAPI, Next.js 15, live di internet.")
    ]
    for i, row in enumerate(data_u, start=1):
        for j, val in enumerate(row):
            cell = table_u.cell(i, j)
            if j == 0:
                set_cell_background(cell, "F1F5F9")
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True

    add_p("", space_after=6)

    # ================= 5. ARSITEKTUR SISTEM =================
    add_h1("5. ARSITEKTUR SISTEM, SKEMA DATABASE & TEKNOLOGI")
    
    add_h2("5.1 Stack Teknologi Terpadu")
    table_stack = doc.add_table(rows=14, cols=4)
    table_stack.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_stack)
    heads_stk = ["Komponen", "Teknologi / Tools", "Versi", "Peran & Justifikasi Arsitektur"]
    for j, h in enumerate(heads_stk):
        c = table_stack.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_stk = [
        ("AI Foundation", "Google Cloud Vertex AI (Gemini 3.8 Flash)", "Production", "Penalaran agen otonom & function calling berlatensi rendah."),
        ("AI Embedding", "Vertex AI text-embedding-005", "768-dim", "Representasi semantik berkualitas tinggi untuk taksonomi MITRE & OWASP."),
        ("Backend Framework", "FastAPI (Python 3.11)", "0.115+", "API asinkronus berkinerja tinggi, Pydantic v2, Swagger docs."),
        ("Database Relasional", "PostgreSQL 16 + pgvector", "16.x / 0.7+", "Penyimpanan data transaksi ACID penuh dan pencarian vektor HNSW."),
        ("Vector Engine", "pgvector Extension", "0.7+", "Pencarian vektor kemiripan kosinus berbasis indeks HNSW."),
        ("SIEM Platform", "Wazuh Manager & Indexer", "4.9.0 / 4.8+", "Agregasi log host & alert jaringan berbasis OpenSearch."),
        ("Lab Target", "OWASP Juice Shop", "17.x", "Lingkungan aplikasi web rentan standar industri untuk uji serangan."),
        ("Reverse Proxy", "Nginx HTTP Proxy", "1.27-alpine", "Penyaring lalu lintas HTTP & penangkap log akses JSON terstruktur (juice_json)."),
        ("Frontend Framework", "Next.js (React 19) + TypeScript", "15.x", "Server-Side Rendering, App Router modern, ter-deploy di Vercel."),
        ("Styling System", "Tailwind CSS + Lucide Icons", "3.4+", "Antarmuka Cyberpunk High-Tech SOC Dark Theme yang ergonomis."),
        ("Data Polling Layer", "SWR (Stale-While-Revalidate)", "2.2+", "Auto-polling adaptif 3 detik tanpa refresh halaman."),
        ("Notifikasi Cepat", "Discord REST API v10 + n8n", "Current", "Kirim notifikasi rich embed darurat ke kanal tim operasional secara asinkronus."),
        ("DevOps & Kontainer", "Docker & Docker Compose", "26.x", "Orkestrasi 6 kontainer modular terisolasi di Google Compute Engine.")
    ]
    for i, row in enumerate(data_stk, start=1):
        for j, val in enumerate(row):
            c = table_stack.cell(i, j)
            if j == 0:
                set_cell_background(c, "F1F5F9")
            set_cell_margins(c, top=70, bottom=70, left=70, right=70)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if j == 0:
                r.bold = True

    add_p("", space_after=6)

    add_h2("5.2 Alur Arsitektur Sistem Ujung-ke-Ujung (End-to-End Flow)")
    add_p(
        "Sistem dibangun dengan arsitektur modular berlapis yang memisahkan antara lapisan persepsi telemetri, "
        "mesin penalaran agen AI, lapisan validasi deterministik, dan lapisan penyajian antarmuka:"
    )
    add_bullet(" Nginx reverse proxy menangkap lalu lintas HTTP lab OWASP Juice Shop dalam format JSON terstruktur, sedangkan sensor Wazuh menangkap log host dan jaringan. Telemetri dialirkan ke backend FastAPI.", bold_prefix="1. Lapisan Persepsi (Sensory Layer):")
    add_bullet(" Backend FastAPI mengelola telemetri yang masuk dan mencatat entitas insiden dengan pengelompokan berbasis alamat IP sumber dan rule ID untuk memitigasi alert storming.", bold_prefix="2. Lapisan Deduplikasi & Ingesti:")
    add_bullet(" Model Gemini 3.8 Flash mengevaluasi alert dan menentukan pemanggilan 4 perkakas forensik secara mandiri (search_alerts_by_ip, get_login_history, inspect_web_attack, mitre_owasp_rag).", bold_prefix="3. Lapisan Penalaran Otonom (Reasoning Core):")
    add_bullet(" Sintesis hasil investigasi diverifikasi oleh Claim Guard. Klaim tanpa rujukan fakta dicoret. Skor keparahan dan keyakinan dihitung secara matematis menggunakan formula deterministik.", bold_prefix="4. Lapisan Penjamin Kebenaran (Deterministic Guard):")
    add_bullet(" Dasbor Next.js 15 mengambil data insiden setiap 3 detik. Analis manusia meninjau Attack Story, matriks bukti Pro vs Contra, dan menekan tombol Approve Mitigation untuk otorisasi tindakan.", bold_prefix="5. Lapisan Presentasi & Tata Kelola (Human-in-the-Loop):")

    add_h2("5.3 Formulasi Matematis: Anti-Halusinasi & Skoring Deterministik")
    add_p(
        "Untuk menjamin objektivitas ilmiah dan kepastian audit, GTNIC SOAR menerapkan formulasi matematis deterministik terprogram "
        "dalam menilai validitas bukti, tingkat keparahan, dan derajat keyakinan:"
    )
    add_p(
        "1. Kriteria Validitas Bukti & Penentuan Status Investigasi:\n"
        "Setiap bukti e wajib memiliki rujukan persis ke himpunan fakta empiris hasil eksekusi alat (evidence_ref ∈ F_empiris). "
        "Bukti pro efektif (E_pro_eff) dibatasi maksimal 2 bukti per perkakas independen guna mencegah dominasi satu sumber.\n"
        "• Status CONFIRMED: Mewajibkan |E_pro_eff| ≥ 2, berasal dari minimal 2 perkakas independen berbeda, dan |E_contra| = 0.\n"
        "• Status LIKELY: Memiliki bukti valid (|E_pro| ≥ 1), namun belum memenuhi seluruh syarat mutlak Confirmed.\n"
        "• Status UNCERTAIN: Jika jumlah perkakas berhasil < 2, atau tidak ada bukti pro valid (|E_pro| = 0), atau terdeteksi inkonsistensi alat.\n"
        "• Status FALSE_POSITIVE: Jika bukti kontra dominan, namun ditahan menjadi UNCERTAIN bila |E_pro| ≥ 2.",
        italic=True, space_before=2, space_after=4
    )
    add_p(
        "2. Perhitungan Skor Keparahan Deterministik (Severity Score / S):\n"
        "S = clamp(10, 100, (L_wazuh × 5) + (min(|E_pro_eff|, 4) × 10) - (min(|E_contra|, 4) × 12) + Δ_confirmed)\n"
        "Di mana L_wazuh adalah tingkat level rule Wazuh (skala 1–15), kontribusi bukti pro efektif bernilai maksimal +40 poin, "
        "penalti bukti kontra bernilai maksimal -48 poin, dan bonus Δ_confirmed = +20 poin diberikan khusus jika status terkonfirmasi (CONFIRMED). "
        "Hasil diklasifikasikan ke dalam: Critical (S ≥ 80), High (60 ≤ S < 80), Medium (40 ≤ S < 60), dan Low (S < 40).",
        italic=True, space_before=2, space_after=4
    )
    add_p(
        "3. Perhitungan Skor Keyakinan Deterministik (Confidence Score / C):\n"
        "C = clamp(0, 100, round(100 × (0.5 × Validity + 0.5 × Coverage)) - P_inconsistent - P_claim)\n"
        "Di mana Validity = |E_valid| / |E_claimed| (rasio klaim yang lolos verifikasi fakta), Coverage = min(1.0, |Tools_digunakan| / 3) "
        "(cakupan keragaman perkakas), P_inconsistent = 20 poin penalti jika ada anomali telemetri, dan P_claim = 10 poin penalti "
        "per temuan frasa tanpa bukti yang dicegat oleh Claim Guard.",
        italic=True, space_before=2, space_after=6
    )

    add_h2("5.4 Skema Basis Data Relasional & Vektor")
    add_p("Penyimpanan data sistem menggunakan 4 tabel utama pada PostgreSQL 16 dengan ekstensi pgvector:")
    add_bullet(" Tabel relasional utama yang menyimpan entitas insiden investigasi lengkap (27 kolom, termasuk raw_alert, status, severity_score, confidence_score, attack_story, pro_evidence, contra_evidence, invalid_evidence, tool_trace, mitre_context, human_decision, decided_by, decided_at, latency_ms).", bold_prefix="1. Tabel incidents:")
    add_bullet(" Knowledge base taksonomi keamanan siber yang menyimpan konten teknik MITRE ATT&CK dan OWASP Top 10 beserta vektor embedding berdimensi 768 dengan indeks HNSW cosine distance.", bold_prefix="2. Tabel security_knowledge:")
    add_bullet(" Tabel deduplikasi cerdas dengan jendela waktu per IP sumber dan rule ID untuk memitigasi badai alert redundan.", bold_prefix="3. Tabel alert_dedup:")
    add_bullet(" Tabel evaluasi performa kuantitatif yang mencatat akurasi klasifikasi, rasio validitas bukti, dan latensi per skenario investigasi.", bold_prefix="4. Tabel benchmark_runs:")

    # ================= 6. BATASAN SISTEM =================
    add_h1("6. BATASAN SISTEM APLIKASI")
    add_p("Untuk menjamin objektivitas evaluasi, batasan sistem GTNIC SOAR dirumuskan sebagai berikut:")
    add_bullet(" Agen secara sengaja dikonfigurasi dalam mode read-only mitigasi. Tombol 'Approve Mitigation' berfungsi mencatat otorisasi analis manusia dan merekam audit trail forensik ke basis data, bukan langsung memodifikasi firewall secara sepihak (integrasi otomasi firewall aktif dijadwalkan pada Roadmap Fase 1).", bold_prefix="1. Prinsip Pertahanan Pasif & Human Approval Gate:")
    add_bullet(" Sensor investigasi web difokuskan pada spektrum OWASP Top 10 utama (SQL Injection dan Cross-Site Scripting pada perkakas agen, serta Path Traversal dan Command Injection pada ingress gateway proxy) yang diuji dari lab OWASP Juice Shop terintegrasi.", bold_prefix="2. Ruang Lingkup Deteksi:")
    add_bullet(" Penalaran semantik tingkat lanjut mengandalkan konektivitas ke Google Cloud Vertex AI. Namun, jika jaringan terputus atau kuota tercapai, sistem secara otomatis beralih ke Local Triage Heuristic Engine sehingga operasional dasar dan penyimpanan insiden tidak terhenti.", bold_prefix="3. Mekanisme Fail-Safe Local Triage:")
    add_bullet(" Dasbor saat ini dioptimalkan untuk satu entitas enterprise (single-tenant) dan belum mendukung partisi data multi-organisasi untuk penyedia MSSP besar.", bold_prefix="4. Arsitektur Multi-Tenant:")

    # ================= 7. TANGKAPAN LAYAR =================
    add_h1("7. TANGKAPAN LAYAR (SCREENSHOT) ANTARMUKA")
    add_p("Berikut adalah dokumentasi antarmuka operasional GTNIC SOAR yang telah ter-deploy publik:")

    add_image_placeholder("TANGKAPAN LAYAR 1: DASHBOARD UTAMA & STATISTIK REAL-TIME", "Gambar 1: Halaman Utama Dasbor GTNIC SOAR dengan Metrik Pemantauan Real-Time dan Antrean Insiden.")
    add_image_placeholder("TANGKAPAN LAYAR 2: DETAIL INSIDEN & ATTACK STORY TIMELINE", "Gambar 2: Rekonstruksi Kronologis Langkah Serangan Siber (Attack Story) yang Dihasilkan oleh Agen AI.")
    add_image_placeholder("TANGKAPAN LAYAR 3: BILATERAL EVIDENCE MATRIX (PRO VS CONTRA)", "Gambar 3: Matriks Bukti Pro vs Kontra dan Referensi Taksonomi MITRE ATT&CK & OWASP.")
    add_image_placeholder("TANGKAPAN LAYAR 4: AUDIT TOOL TRACE & TOMBOL PERSETUJUAN", "Gambar 4: Jejak Audit Eksekusi Perkakas Agen dan Panel Tindakan Persetujuan Analis Manusia.")
    add_image_placeholder("TANGKAPAN LAYAR 5: NOTIFIKASI DARURAT DISCORD BOT", "Gambar 5: Notifikasi Darurat Berformat Rich Embed pada Kanal Komunikasi Operasional Discord.")

    # ================= 8. RENCANA PENGEMBANGAN =================
    add_h1("8. RENCANA PENGEMBANGAN LANJUTAN (FUTURE DEVELOPMENT)")
    add_p("Peta jalan pengembangan strategis GTNIC SOAR untuk implementasi skala industri terbagi ke dalam 5 fase terukur:")

    table_f = doc.add_table(rows=6, cols=3)
    table_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_f)
    headers_f = ["Fase & Target Waktu", "Target Inovasi", "Deskripsi & Dampak Industri"]
    for j, h in enumerate(headers_f):
        cell = table_f.cell(0, j)
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_f = [
        ("Fase 1: Q1 2027", "Active Response Firewall Automation", "Integrasi aksi Approve Mitigation langsung ke Cloudflare WAF, AWS Security Group, dan Wazuh Active Response untuk isolasi IP penyerang otomatis <1 detik."),
        ("Fase 2: Q2 2027", "Threat Intelligence Feeds Enrichment", "Integrasi perkakas agen ke API VirusTotal, AbuseIPDB, Shodan, dan AlienVault OTX untuk verifikasi reputasi ancaman global secara real-time."),
        ("Fase 3: Q3 2027", "Automated Executive PDF Compliance Report", "Modul generator laporan kepatuhan regulasi UU PDP dan standar ISO 27001 berformat PDF resmi bertanda tangan digital untuk kebutuhan audit dan CISO."),
        ("Fase 4: Q4 2027", "Multi-Tenant MSSP & Enterprise RBAC", "Arsitektur multi-penyewa dengan kontrol akses berbasis peran (Tier-1, Tier-2, Manager) untuk melayani puluhan klien enterprise dalam satu platform."),
        ("Fase 5: 2028", "Adaptive Autonomous Honeypot Deception", "Kapabilitas agen untuk mengalihkan peretas tingkat tinggi (APT) ke sistem umpan tiruan guna mempelajari taktik baru tanpa membahayakan data inti.")
    ]
    for i, row in enumerate(data_f, start=1):
        for j, val in enumerate(row):
            cell = table_f.cell(i, j)
            if j == 0:
                set_cell_background(c, "F1F5F9")
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(9)
            if j == 0:
                r.bold = True

    add_p("", space_after=6)

    # ================= 9. TAUTAN PENTING =================
    add_h1("9. TAUTAN PENTING (LAMPIRAN)")
    add_p("Sebagai bahan verifikasi dan evaluasi menyeluruh Dewan Juri GTNIC 2026, berikut adalah tautan proyek kami:")
    add_bullet(" https://gtnic-hackwitgoh.vercel.app/ (Aktif 24/7 di jaringan Vercel Edge dan dapat diuji langsung oleh Dewan Juri).", bold_prefix="• Tautan Sistem / Prototype Live: ")
    add_bullet(" https://juice.flummox.cloud/ (Lab aplikasi web target yang terintegrasi langsung dengan sensor reverse proxy).", bold_prefix="• Tautan Lingkungan Lab Serangan (OWASP Juice Shop): ")
    add_bullet(" [Tautan Repositori GitHub Anda — Pastikan Mode Akses Publik]", bold_prefix="• Tautan Repositori / Dokumentasi Lengkap: ")
    add_bullet(" [Tautan Video Demo YouTube (Mode Publik atau Unlisted)]", bold_prefix="• Tautan Video Demo YouTube: ")

    add_h2("DAFTAR PUSTAKA")
    cites = [
        "1. AwanPintar.id. (2026). Laporan Lanskap Ancaman dan Serangan Siber Indonesia Semester I 2026. Jakarta: PT Media Antar Nusa.",
        "2. Badan Siber dan Sandi Negara (BSSN). (2025). Laporan Tahunan Lanskap Keamanan Siber Nasional 2024–2025. Jakarta: Direktorat Operasi Keamanan Siber, BSSN RI.",
        "3. Badan Siber dan Sandi Negara (BSSN). (2026). Statistik Anomali Siber Nasional Kuartal I 2026. Jakarta: Pusat Operasi Keamanan Siber Nasional, BSSN RI.",
        "4. IBM Security. (2024). Cost of a Data Breach Report 2024. Ponemon Institute & IBM Security Services.",
        "5. ISC2. (2024). ISC2 Cybersecurity Workforce Study 2024: Addressing the Global Talent Shortage and the Impact of Emerging Tech. Clearwater, FL: International Information System Security Certification Consortium.",
        "6. MITRE Corporation. (2025). MITRE ATT&CK Framework: Enterprise Matrix v15. Bedford, MA: The MITRE Corporation.",
        "7. OWASP Foundation. (2021). OWASP Top 10:2021 The Ten Most Critical Web Application Security Risks. The Open Web Application Security Project.",
        "8. Republik Indonesia. (2022). Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi. Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196.",
        "9. Touvron, H., dkk. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv preprint arXiv:2307.09288.",
        "10. Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations (ICLR 2023)."
    ]
    for c in cites:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.line_spacing = 1.15
        p_c.paragraph_format.space_after = Pt(4)
        p_c.paragraph_format.left_indent = Cm(0.75)
        p_c.paragraph_format.first_line_indent = Cm(-0.75)
        r = p_c.add_run(c)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    output_path = "docs/GTNIC2026_Proposal_GTNIC_SOAR_v2.docx"
    doc.save(output_path)
    print(f"Successfully generated expanded proposal docx at: {output_path}")
    try:
        doc.save("docs/GTNIC2026_Proposal_GTNIC_SOAR.docx")
        print("Also updated docs/GTNIC2026_Proposal_GTNIC_SOAR.docx")
    except Exception as e:
        print(f"Note: docs/GTNIC2026_Proposal_GTNIC_SOAR.docx is currently opened in another app ({e}). Please use _v2.docx or close Word.")

if __name__ == "__main__":
    build_full_proposal()
