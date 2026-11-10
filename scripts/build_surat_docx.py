import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_surat():
    doc = docx.Document()
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(3.0)

    def add_p(text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=3, space_before=0, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    add_p("SURAT PERNYATAAN KEASLIAN KARYA", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p("GARDA TECH NATIONAL INNOVATION COMPETITION (GTNIC) 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

    add_p("Yang bertanda tangan di bawah ini:")
    add_p("Ketua Tim:", bold=True, space_before=4)
    add_p("  Nama Lengkap               : [Nama Ketua Tim]")
    add_p("  NIM / NPM                  : [NIM/NPM Ketua]")
    add_p("  Perguruan Tinggi / Sekolah : [Nama Kampus / Sekolah]")
    add_p("  Program Studi / Jurusan    : [Jurusan]")
    add_p("  Nomor Telepon / WhatsApp   : [Nomor HP]")
    add_p("  Email Aktif                : [Alamat Email Aktif]")

    add_p("Anggota 1:", bold=True, space_before=4)
    add_p("  Nama Lengkap               : [Nama Anggota 1]")
    add_p("  NIM / NPM                  : [NIM/NPM Anggota 1]")
    add_p("  Perguruan Tinggi / Sekolah : [Nama Kampus / Sekolah]")

    add_p("Anggota 2:", bold=True, space_before=4)
    add_p("  Nama Lengkap               : [Nama Anggota 2]")
    add_p("  NIM / NPM                  : [NIM/NPM Anggota 2]")
    add_p("  Perguruan Tinggi / Sekolah : [Nama Kampus / Sekolah]")

    add_p("Identitas Karya:", bold=True, space_before=6)
    add_p("  Nama Tim                   : [NAMA TIM ANDA]")
    add_p("  Kategori Kompetisi         : AI Agent Development")
    add_p("  Sub-Tema                   : \"Building Intelligent AI Agents for Enterprise Productivity\"")
    add_p("  Judul Karya                : GTNIC SOAR: Autonomous AI SOC Agent untuk Otomasi Investigasi Ancaman Siber Enterprise Berbasis Multi-Tool Calling dan Anti-Halusinasi Deterministik")

    add_p("Dengan ini menyatakan dengan sesungguhnya dan penuh kesadaran bahwa:", space_before=6)
    points = [
        "1. Karya yang kami ajukan dalam Garda Tech National Innovation Competition (GTNIC) 2026 adalah benar-benar karya orisinil ciptaan kami dan bukan hasil penjiplakan, fabrikasi, pemalsuan, atau plagiarisme dari karya pihak lain dalam bentuk apa pun.",
        "2. Seluruh modul perangkat lunak, arsitektur agen, skema integrasi alat (tool calling), antarmuka web, serta dokumen pendukung yang kami sertakan merupakan hasil kerja mandiri tim kami dengan memanfaatkan pustaka open-source sesuai ketentuan lisensi.",
        "3. Karya ini belum pernah menjuarai kompetisi teknologi tingkat regional, nasional, maupun internasional lainnya, dan tidak sedang diikutsertakan dalam kompetisi sejenis yang sedang berlangsung.",
        "4. Karya ini tidak melanggar Hak Kekayaan Intelektual (HAKI), hak cipta, merek dagang, kerahasiaan data, maupun ketentuan perundang-undangan yang berlaku di Negara Kesatuan Republik Indonesia.",
        "5. Apabila di kemudian hari ditemukan bukti ketidakbenaran dari pernyataan ini, kami bersedia menerima sanksi diskualifikasi dari GTNIC 2026, pembatalan status pemenang, serta konsekuensi hukum yang berlaku."
    ]
    for pt in points:
        add_p(pt, space_after=3)

    add_p("Demikian surat pernyataan ini kami buat dengan sebenarnya, dalam keadaan sehat, sadar, dan tanpa paksaan dari pihak mana pun, untuk dipergunakan sebagaimana mestinya.", space_before=4, space_after=10)

    add_p("[Kota Domisili], 10 November 2026", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=12)
    
    # Signature table for layout
    table = doc.add_table(rows=1, cols=2)
    table.alignment = docx.enum.table.WD_TABLE_ALIGNMENT.CENTER
    c1 = table.cell(0, 0)
    c2 = table.cell(0, 1)
    
    p1 = c1.paragraphs[0]
    p1.add_run("Menyatakan,\n\n\n[Materai Rp10.000]\n\n\n\n( [Nama Ketua Tim] )\nKetua Tim")
    
    p2 = c2.paragraphs[0]
    p2.add_run("Mengetahui Anggota:\n\n\n\n( [Nama Anggota 1] )\nAnggota 1\n\n( [Nama Anggota 2] )\nAnggota 2")

    doc.save("docs/Surat_Pernyataan_Keaslian_Karya.docx")
    print("Successfully generated docs/Surat_Pernyataan_Keaslian_Karya.docx")

if __name__ == "__main__":
    create_surat()
