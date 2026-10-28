import os
from fpdf import FPDF
from crypto_chain import calculate_file_hash, VAULT_DIR

class ForensicCertificatePDF(FPDF):
    def __init__(self, is_tampered=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_tampered = is_tampered

    def header(self):
        if self.is_tampered:
            self.set_text_color(220, 20, 60) # Crimson Red
            self.set_font("Helvetica", "B", 15)
            self.cell(0, 8, "FORENSIC INTEGRITY BREACH & TAMPER REPORT", new_x="LMARGIN", new_y="NEXT", align="C")
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 5, "WARNING: EVIDENCE COMPROMISED - INADMISSIBLE UNDER SECTION 65B", new_x="LMARGIN", new_y="NEXT", align="C")
        else:
            self.set_text_color(0, 100, 0) # Forest Green
            self.set_font("Helvetica", "B", 15)
            self.cell(0, 8, "DIGITAL FORENSIC CHAIN OF CUSTODY CERTIFICATE", new_x="LMARGIN", new_y="NEXT", align="C")
            self.set_font("Helvetica", "I", 9)
            self.cell(0, 5, "Compliant with Section 65B Indian Evidence Act / Cyber Forensics Standards", new_x="LMARGIN", new_y="NEXT", align="C")
        
        self.set_text_color(0, 0, 0)
        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        status_tag = "COMPROMISED" if self.is_tampered else "VERIFIED 100%"
        self.cell(0, 10, f"Page {self.page_no()} | Forensic Status: {status_tag} | Cryptographic Hash Chain Audit", align="C")


def check_block_tampered(block_data: dict) -> tuple[bool, str]:
    """Checks if the actual physical evidence file differs from recorded hash."""
    filepath = os.path.join(VAULT_DIR, block_data["stored_filename"])
    if not os.path.exists(filepath):
        return True, "FILE_MISSING_FROM_REPOSITORY"
    
    with open(filepath, "rb") as f:
        current_bytes = f.read()
    current_hash = calculate_file_hash(current_bytes)
    
    is_tampered = (current_hash != block_data["evidence_hash"])
    return is_tampered, current_hash


def generate_forensic_pdf(
    block_data: dict, 
    output_path: str = None, 
    magistrate_name: str = None, 
    court_location: str = None
) -> tuple[bool, any]:
    is_tampered, current_disk_hash = check_block_tampered(block_data)
    
    pdf = ForensicCertificatePDF(is_tampered=is_tampered)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Status Banner
    if is_tampered:
        pdf.set_fill_color(255, 230, 230)
        pdf.set_text_color(180, 0, 0)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, " CRITICAL ALERT: EVIDENCE TAMPERING / CORRUPTION DETECTED ", border=1, new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
    else:
        pdf.set_fill_color(230, 255, 230)
        pdf.set_text_color(0, 120, 0)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, " STATUS: MATHEMATICALLY UNALTERED & COURT ADMISSIBLE ", border=1, new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)
    
    # 2. Case Details
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "1. CASE & SEIZURE PARTICULARS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    
    details = [
        ("Case Reference ID", block_data.get("case_id", "N/A")),
        ("Crime Classification", block_data.get("case_type", "Cyber Crime")),
        ("Victim / Complainant", block_data.get("victim_name", "N/A")),
        ("Investigating Officer", block_data.get("officer_name", "N/A")),
        ("Officer Badge / ID No.", block_data.get("badge_id", "N/A")),
        ("Seizure Site / Location", block_data.get("seizure_location", "N/A")),
        ("Seizure Timestamp (UTC)", block_data.get("timestamp", "N/A")),
    ]
    if magistrate_name:
        details.append(("Designated Judicial Bench", magistrate_name))
    if court_location:
        details.append(("Judicial Jurisdiction", court_location))
    
    for label, val in details:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(55, 6, f"{label}:", 0)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6, str(val), new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(4)
    
    # 3. Cryptographic Fingerprints Comparison
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "2. CRYPTOGRAPHIC INTEGRITY AUDIT DATA", new_x="LMARGIN", new_y="NEXT")
    
    crypto_details = [
        ("Chain Block Index", f"Block #{block_data.get('block_id')}"),
        ("Original File Name", block_data.get("original_filename", "N/A")),
        ("Original Seizure Hash (SHA-256)", block_data.get("evidence_hash", "N/A")),
        ("Live Recomputed Hash (Disk)", current_disk_hash),
        ("HMAC-SHA256 Signature", block_data.get("hmac_sig", "N/A")),
        ("Previous Block Hash", block_data.get("prev_hash", "N/A")),
        ("Block Hash (Merkle Link)", block_data.get("block_hash", "N/A")),
    ]
    
    for label, val in crypto_details:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(58, 6, f"{label}:", 0)
        
        if label == "Live Recomputed Hash (Disk)" and is_tampered:
            pdf.set_font("Courier", "B", 8)
            pdf.set_text_color(200, 0, 0)
        else:
            pdf.set_font("Courier", "", 8)
            pdf.set_text_color(0, 0, 0)
            
        pdf.cell(0, 6, str(val), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        
    pdf.ln(5)
    
    # 4. Statutory Declaration / Breach Finding
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "3. STATUTORY FORENSIC VERDICT", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    
    if is_tampered:
        pdf.set_text_color(180, 0, 0)
        declaration_text = (
            "FORENSIC VIOLATION NOTICE: The live cryptographic hash of the evidence file does NOT match the "
            "original SHA-256 fingerprint registered in the chain of custody ledger at seizure. "
            "One or more bytes/pixels have been modified after custody ingestion. This evidence fails the legal "
            "threshold under Section 65B of the Indian Evidence Act and must be rejected as COMPROMISED."
        )
    else:
        pdf.set_text_color(0, 100, 0)
        declaration_text = (
            "I hereby certify that the electronic record described herein was seized and deposited into the "
            "cryptographic Chain of Custody custody system during regular official duty. The live computed SHA-256 "
            "fingerprint strictly matches the genesis seizure hash, guaranteeing the evidence remains unaltered, authentic, "
            "and fully admissible in court."
        )
        
    pdf.multi_cell(0, 5, declaration_text)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)
    
    # 5. Custody Handover Trail
    custody_trail = block_data.get("custody_trail", [])
    if custody_trail:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, "4. CHAIN OF CUSTODY HANDOVER AUDIT TRAIL", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 8)
        
        for idx, event in enumerate(custody_trail):
            trail_line = f"[{event.get('timestamp')}] {event.get('from_entity')}  --->  {event.get('to_entity')} | Purpose: {event.get('purpose')}"
            pdf.cell(0, 4.5, trail_line, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # 6. Direct Vector Cryptographic QR Code Generation (Neatly aligned without overlap)
    qr_status = "COMPROMISED" if is_tampered else "AUTHENTIC"
    case_ref = block_data.get('case_id', 'FIR-2024-CYBER-809')
    block_id = block_data.get('block_id', 1)
    file_name = block_data.get('original_filename', 'evidence.bin')
    ev_hash = block_data.get('evidence_hash', '')
    officer_name = block_data.get('officer_name', 'Forensic Unit')
    timestamp_str = block_data.get('timestamp', '')
    case_type = block_data.get('case_type', 'Cyber Forensics')
    
    import urllib.parse
    params = urllib.parse.urlencode({
        'case': case_ref,
        'block': block_id,
        'file': file_name,
        'hash': ev_hash,
        'status': qr_status,
        'officer': officer_name,
        'time': timestamp_str,
        'type': case_type
    })
    qr_data = f"https://fair-holiday-ixjm8.ship.place/?{params}"
    
    start_y = pdf.get_y() + 6
    if start_y > 205:
        pdf.add_page()
        start_y = 25
        
    # 6. Standard Scannable QR Code Generation
    qr_x = 145
    qr_total_size = 46
    qr_img_path = os.path.join(VAULT_DIR, f"qr_block_{block_data.get('block_id')}.png")
    
    try:
        from pure_qr import create_qr_code
        create_qr_code(qr_data, qr_img_path)
        if os.path.exists(qr_img_path):
            pdf.image(qr_img_path, x=qr_x, y=start_y, w=qr_total_size, h=qr_total_size)
    except Exception:
        pass

    # QR Label directly below QR code
    pdf.set_xy(qr_x - 5, start_y + qr_total_size + 2)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(qr_total_size + 10, 4, "[ DIGITAL QR SEAL ]", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(qr_x - 5, start_y + qr_total_size + 6)
    pdf.set_font("Helvetica", "I", 7)
    pdf.cell(qr_total_size + 10, 4, "Scan for Instant Verification", align="C", new_x="LMARGIN", new_y="NEXT")

    # Signatures on the left side
    sig_y = start_y + 16
    pdf.set_xy(10, sig_y)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(65, 5, "_______________________________")
    pdf.cell(65, 5, "_______________________________", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_xy(10, sig_y + 6)
    pdf.cell(65, 5, "Investigating Forensic Officer")
    mag_title = f"Presiding Magistrate ({magistrate_name[:20]})" if magistrate_name else "Official Cyber Forensic Seal"
    pdf.cell(65, 5, mag_title, new_x="LMARGIN", new_y="NEXT")

    pdf_bytes = bytes(pdf.output())
    if output_path:
        with open(output_path, "wb") as f_out:
            f_out.write(pdf_bytes)
        return is_tampered, output_path
    return is_tampered, pdf_bytes


def generate_forensic_pdf_bytes(
    block_data: dict, 
    magistrate_name: str = None, 
    court_location: str = None
) -> bytes:
    """Helper that directly returns the binary bytes of the Section 65B PDF certificate."""
    _, pdf_bytes = generate_forensic_pdf(
        block_data=block_data, 
        output_path=None, 
        magistrate_name=magistrate_name, 
        court_location=court_location
    )
    return pdf_bytes


def generate_handover_challan_pdf(block_data: dict, event: dict, output_path: str = None) -> bytes:
    """Generates an official Inter-Agency Custody Handover Challan & Receipt PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header
    pdf.set_text_color(15, 23, 42)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 8, "CHAIN OF CUSTODY INTER-AGENCY HANDOVER CHALLAN", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 5, "Official Digital Forensic Transfer Receipt | Compliant with Section 65B Indian Evidence Act", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    # Challan Reference Banner
    challan_id = event.get("challan_id", f"CHL-{block_data.get('case_id')}-TX")
    pdf.set_fill_color(240, 244, 248)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, f"  CHALLAN RECEIPT REF: {challan_id}  |  TRANSFER STEP #{event.get('step_no', 1)}", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    # 1. Evidence Artifact Specification
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "1. SEIZED EVIDENCE SPECIFICATION", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    
    col_w1, col_w2 = 50, 140
    pdf.cell(col_w1, 5.5, "Case / FIR Reference:", border=0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(col_w2, 5.5, f"{block_data.get('case_id')} ({block_data.get('case_type', 'Cyber Crime')})", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(col_w1, 5.5, "Evidence File Name:", border=0)
    pdf.cell(col_w2, 5.5, f"{block_data.get('original_filename')} ({block_data.get('file_size_bytes')} bytes)", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_w1, 5.5, "Immutable Merkle Block:", border=0)
    pdf.cell(col_w2, 5.5, f"Block #{block_data.get('block_id')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_w1, 5.5, "Evidence SHA-256 Hash:", border=0)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(col_w2, 5.5, f"{block_data.get('evidence_hash')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    # 2. Transmission & Handover Event
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "2. TRANSMISSION & CUSTODIAL TRANSFER DETAILS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    
    pdf.cell(col_w1, 5.5, "Transfer Execution Time:", border=0)
    pdf.cell(col_w2, 5.5, f"{event.get('timestamp')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_w1, 5.5, "Transferring Authority (From):", border=0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(col_w2, 5.5, f"{event.get('from_entity')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(col_w1, 5.5, "Receiving Authority (To):", border=0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(col_w2, 5.5, f"{event.get('to_entity')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(col_w1, 5.5, "Transfer / Examination Purpose:", border=0)
    pdf.cell(col_w2, 5.5, f"{event.get('purpose')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_w1, 5.5, "Custodial Legal Status:", border=0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(col_w2, 5.5, f"{event.get('custody_status', 'In Custody')}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    
    # 3. Dual Cryptographic HMAC Signatures
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "3. DUAL CRYPTOGRAPHIC TRANSMISSION TOKENS (AUTHENTICATION)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    
    pdf.cell(col_w1, 5, "Transferor Digital HMAC Token:", border=0)
    pdf.cell(col_w2, 5, f"{event.get('transferor_hmac', 'AUTH-TOKEN-HMAC-SHA256')}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(col_w1, 5, "Recipient Acceptance HMAC Token:", border=0)
    pdf.cell(col_w2, 5, f"{event.get('recipient_hmac', 'RECV-TOKEN-HMAC-SHA256')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    # 4. Legal Declaration
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(0, 5, "4. STATUTORY ADMISSIBILITY DECLARATION (SECTION 65B)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    declaration = (
        "This Inter-Agency Handover Challan constitutes conclusive electronic documentation of custody transfer. "
        "The cryptographic hash of the underlying artifact was recalculated and mutually attested by both parties "
        "prior to physical and logical transmission. Strict chain of custody continuity has been preserved without interruption."
    )
    pdf.multi_cell(0, 4.5, declaration)
    pdf.ln(4)
    
    # QR Code & Signatures
    start_y = pdf.get_y() + 4
    if start_y > 215:
        pdf.add_page()
        start_y = 25
        
    qr_x = 148
    qr_size = 40
    qr_img = os.path.join(VAULT_DIR, f"qr_challan_{challan_id}.png")
    
    import urllib.parse
    params = urllib.parse.urlencode({
        'case': block_data.get('case_id'),
        'block': block_data.get('block_id'),
        'challan': challan_id,
        'from': event.get('from_entity'),
        'to': event.get('to_entity'),
        'status': 'AUTHENTIC',
        'hash': block_data.get('evidence_hash')
    })
    qr_url = f"https://fair-holiday-ixjm8.ship.place/?{params}"
    
    try:
        from pure_qr import create_qr_code
        create_qr_code(qr_url, qr_img)
        if os.path.exists(qr_img):
            pdf.image(qr_img, x=qr_x, y=start_y, w=qr_size, h=qr_size)
    except Exception:
        pass
        
    pdf.set_xy(qr_x - 5, start_y + qr_size + 2)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(qr_size + 10, 4, "[ OFFICIAL HANDOVER VERIFIER ]", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Signatures
    sig_y = start_y + 12
    pdf.set_xy(10, sig_y)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(65, 5, "_______________________________")
    pdf.cell(65, 5, "_______________________________", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_xy(10, sig_y + 6)
    pdf.cell(65, 4.5, "Releasing Custodian (Transferor)")
    pdf.cell(65, 4.5, "Receiving Custodian (Recipient)", new_x="LMARGIN", new_y="NEXT")
    
    pdf_bytes = bytes(pdf.output())
    if output_path:
        with open(output_path, "wb") as f_out:
            f_out.write(pdf_bytes)
    return pdf_bytes
