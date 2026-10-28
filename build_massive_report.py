import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_massive_report():
    src_path = r"C:\Users\kavin\.gemini\antigravity\brain\b37fd18a-0194-4357-93a6-9e420b486c27\.user_uploaded\media_1792470831284_3cb0c08d.docx"
    doc = Document(src_path)

    # 1. COVER PAGE: PRESERVE DRAWINGS IN P0 & P4
    p0 = doc.paragraphs[0]
    if len(p0.runs) >= 4:
        p0.runs[2].text = ""
        p0.runs[3].text = "CRYPTOGRAPHIC CHAIN OF CUSTODY SYSTEM"
        p0.runs[3].font.name = "Times New Roman"
        p0.runs[3].font.size = Pt(17)
        p0.runs[3].bold = True

    p1 = doc.paragraphs[1]
    if len(p1.runs) >= 1:
        p1.runs[0].text = "FOR DIGITAL FORENSICS IN CLOUD ENVIRONMENTS"
        p1.runs[0].font.name = "Times New Roman"
        p1.runs[0].font.size = Pt(17)
        p1.runs[0].bold = True

    # P4 has middle drawings. Leave untouched!

    # Table 0: Student names
    t0 = doc.tables[0]
    t0.rows[0].cells[0].text = "KAVIN. R"
    t0.rows[0].cells[1].text = "(922523205061)"
    t0.rows[1].cells[0].text = "KESHAV. A. T"
    t0.rows[1].cells[1].text = "(922523205064)"

    for r_idx in range(2):
        for cell in t0.rows[r_idx].cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(12)
                    r.bold = True

    tbl0 = t0._tbl
    trs = list(tbl0.xpath('./w:tr'))
    if len(trs) > 2:
        for tr in trs[2:]:
            tbl0.remove(tr)

    # Paragraph 21: Year on Cover Page
    if len(doc.paragraphs) > 21:
        p21 = doc.paragraphs[21]
        p21.text = "                                                  MAY 2026"
        for r in p21.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
            r.bold = True

    # 2. BONAFIDE CERTIFICATE (Paragraph 26)
    p26 = doc.paragraphs[26]
    p26.text = (
        "Certified that this project report titled “CRYPTOGRAPHIC CHAIN OF CUSTODY SYSTEM FOR DIGITAL FORENSICS "
        "IN CLOUD ENVIRONMENTS” is the bonafide work of “KAVIN. R (922523205061) and KESHAV. A. T (922523205064)” "
        "who carried out under my supervision."
    )
    p26.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p26.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    # 3. ABSTRACT (Paragraphs 96-99)
    doc.paragraphs[96].text = (
        "Cryptographic Chain of Custody System for Digital Forensics in Cloud Environments is an enterprise-grade defense platform "
        "that mathematically guarantees the integrity, non-repudiation, and legal admissibility of electronic evidence. In modern criminal, "
        "financial, and corporate cyber investigations, digital artifacts—such as CCTV video recordings, virtual machine disk bitstreams, "
        "intrusion access logs, and mobile phone extractions—are prone to allegations of post-seizure tampering under Section 65B of the "
        "Indian Evidence Act / Bharatiya Sakshya Adhiniyam, 2023. The system solves this crisis by deploying a zero-gas Merkle hash-chain "
        "ledger that records every evidence artifact upon seizure with an unbreakable chronological link."
    )
    doc.paragraphs[97].text = (
        "The platform incorporates an AI Binary Magic-Byte Forensics Scanner that pre-scans file byte offsets (0x00 to 0x40) to instantly detect "
        "Trojan executables (Windows PE 'MZ' binaries, Linux ELF payloads, PHP web shells) disguised under innocent image or PDF extensions. "
        "Seized artifacts are mirrored synchronously across a dual-vault architecture comprising an on-premises physical vault and an encrypted "
        "cloud repository, cryptographically bound using NIST-standard SHA-256 digests and secret-keyed HMAC message authentication tokens."
    )
    doc.paragraphs[98].text = (
        "An Autonomous Disaster Recovery Engine continuously monitors file integrity and automatically self-heals corrupted or tampered "
        "local files from pristine cloud replicas in an average of 0.626 milliseconds. To ensure seamless judicial collaboration, the platform "
        "features a Dual-Party Cryptographic Custody Handover Protocol requiring mutual digital signatures (Transferor PIN and Recipient Token) "
        "and auto-generates official Inter-Agency Handover Challan receipts and Section 65B Compliance Certificates. Every generated PDF embeds "
        "a high-density QR seal that instantly redirects smartphone cameras to a live public cloud verification portal (https://fair-holiday-ixjm8.ship.place/)."
    )
    doc.paragraphs[99].text = (
        "The system also provides an interactive visual Plotly Merkle Tree node graph, a Reverse Hash Search Engine ('Know Your Evidence'), and a "
        "Crime Scene Forensic Geolocation Satellite Map. Comprehensive automated stress testing across 870 test cycles verified a 100% pass rate "
        "with zero false positives and zero tamper escape rates. After successful completion of the project, PO1 through PO12 and PSO1 through PSO3 "
        "are effectively attained."
    )

    for p_idx in [96, 97, 98, 99]:
        doc.paragraphs[p_idx].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for r in doc.paragraphs[p_idx].runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

    # 4. TABLE 1: TABLE OF CONTENTS
    t1 = doc.tables[1]
    t1.rows[5].cells[1].text = "Background of Cloud Forensics & Chain of Custody"
    t1.rows[6].cells[1].text = "Cryptographic Hash-Chaining & Merkle Trees in Forensics"
    t1.rows[7].cells[1].text = "Importance of Admissible Digital Evidence & Section 65B"
    t1.rows[27].cells[1].text = "Algorithm and Cryptographic Models (SHA-256 / Merkle / HMAC)"

    for r_idx in [5, 6, 7, 27]:
        for cell in t1.rows[r_idx].cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10)

    # 5. REMOVE OLD BODY ELEMENTS AFTER TABLE 1
    body = doc._body._body
    t1_elem = t1._tbl
    t1_idx = body.index(t1_elem)
    elements_to_remove = [child for child in body[t1_idx + 1:-1]]
    for el in elements_to_remove:
        body.remove(el)
    print(f"Removed {len(elements_to_remove)} old paragraphs after Table 1.")

    # 6. HELPER FUNCTIONS
    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_after=6, space_before=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        return p

    # Read and insert full expanded chapters from a structured text module
    # We will generate comprehensive, full-length content for each chapter:
    from massive_academic_chapters import build_all_chapters
    build_all_chapters(doc, add_p, add_h1, add_h2, add_h3)

    out_file = "VSB_IT_Cryptographic_Chain_of_Custody_Full_Report.docx"
    doc.save(out_file)
    print(f"Full Report successfully compiled and saved to '{out_file}'!")
    return out_file

if __name__ == "__main__":
    generate_massive_report()
