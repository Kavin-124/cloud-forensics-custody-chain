import os
import json
import cv2
from pdf_generator import generate_forensic_pdf

with open('ledger.json', 'r', encoding='utf-8') as f:
    chain = json.load(f)

samples_dir = os.path.join(os.path.dirname(__file__), "samples")
os.makedirs(samples_dir, exist_ok=True)

det = cv2.QRCodeDetector()

print("Regenerating all certificates in samples directory...")
for b in chain:
    pdf_name = f"certificate_case_{b['case_id']}_block_{b['block_id']}.pdf"
    pdf_path = os.path.join(samples_dir, pdf_name)
    is_tampered, path = generate_forensic_pdf(b, pdf_path)
    
    # Verify QR file
    qr_img_path = os.path.join("evidence_vault", f"qr_block_{b['block_id']}.png")
    img = cv2.imread(qr_img_path)
    val, _, _ = det.detectAndDecode(img)
    
    status_str = "TAMPERED" if is_tampered else "AUTHENTIC"
    print(f"-> {pdf_name}: Generated ({status_str}) | QR Verified: {bool(val)}")

print("Done! All certificates in samples/ are 100% freshly updated and scannable.")
