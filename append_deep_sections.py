# Append deep technical content, tables, algorithms, and code listings into generate_chapters_content.py
import re

extra_code = '''
    # =========================================================================
    # APPENDIX: SOURCE CODE IMPLEMENTATION & DATA SCHEMAS
    # =========================================================================
    add_h1("APPENDIX")
    add_h2("A.1 Cryptographic Chain of Custody Core Implementation (crypto_chain.py)")
    add_p("The following Python source listing implements the core NIST SHA-256 hashing, secret-keyed HMAC message authentication, sequential Merkle chaining, and AI magic-byte inspection algorithms:")
    
    code_snippet = (
        "import hashlib\\n"
        "import hmac\\n"
        "import json\\n"
        "import os\\n"
        "from datetime import datetime\\n\\n"
        "SECRET_HMAC_KEY = b\\"FORENSIC_SECRET_KEY_CYBER_CRIME_CELL_2024\\"\\n"
        "VAULT_DIR = \\\"evidence_vault\\\"\\n"
        "CLOUD_VAULT_DIR = \\\"cloud_vault\\\"\\n"
        "LEDGER_FILE = \\\"ledger.json\\\"\\n\\n"
        "def calculate_file_hash(file_bytes: bytes) -> str:\\n"
        "    sha256 = hashlib.sha256()\\n"
        "    sha256.update(file_bytes)\\n"
        "    return sha256.hexdigest()\\n\\n"
        "def generate_hmac(data_str: str) -> str:\\n"
        "    return hmac.new(SECRET_HMAC_KEY, data_str.encode(\\\"utf-8\\\"), hashlib.sha256).hexdigest()\\n\\n"
        "def calculate_block_hash(block_data: dict) -> str:\\n"
        "    payload = f\\\"{block_data['block_id']}_{block_data['timestamp']}_{block_data['case_id']}_{block_data['evidence_hash']}_{block_data['prev_hash']}\\\"\\n"
        "    return hashlib.sha256(payload.encode(\\\"utf-8\\\")).hexdigest()\\n\\n"
        "def detect_magic_bytes(file_bytes: bytes, filename: str) -> dict:\\n"
        "    ext = os.path.splitext(filename)[1].lower().strip(\\\".\\\")\\n"
        "    sample = file_bytes[:32]\\n"
        "    if sample.startswith(b\\\"\\\\xFF\\\\xD8\\\\xFF\\\"):\\n"
        "        true_type, expected = \\\"JPEG Image (JFIF / EXIF)\\\", [\\\"jpg\\\", \\\"jpeg\\\"]\\n"
        "    elif sample.startswith(b\\\"\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n\\\"):\\n"
        "        true_type, expected = \\\"PNG Image\\\", [\\\"png\\\"]\\n"
        "    elif sample.startswith(b\\\"%PDF-\\\"):\\n"
        "        true_type, expected = \\\"PDF Document\\\", [\\\"pdf\\\"]\\n"
        "    elif sample.startswith(b\\\"MZ\\\"):\\n"
        "        true_type, expected = \\\"Windows PE Executable / Malware Binary\\\", [\\\"exe\\\", \\\"dll\\\"]\\n"
        "    elif sample.startswith(b\\\"\\\\x7FELF\\\"):\\n"
        "        true_type, expected = \\\"Linux ELF Binary Payload\\\", [\\\"elf\\\", \\\"bin\\\"]\\n"
        "    is_spoofed = (ext not in expected) if expected and ext else False\\n"
        "    return {\\\"true_type\\\": true_type, \\\"is_spoofed\\\": is_spoofed}\\n"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.space_before = Pt(6)
    p_code.paragraph_format.space_after = Pt(8)
    p_code.paragraph_format.line_spacing = 1.15
    run_code = p_code.add_run(code_snippet)
    run_code.font.name = "Courier New"
    run_code.font.size = Pt(9.5)
    run_code.font.color.rgb = RGBColor(0, 51, 102)

    add_h2("A.2 Immutable Ledger JSON Block Schema")
    add_p("Every seized digital evidence item is recorded into `ledger.json` adhering to the following cryptographically validated schema:")
    
    schema_snippet = (
        "{\\n"
        '  "block_id": 1,\\n'
        '  "timestamp": "2026-10-20 04:07:42 UTC",\\n'
        '  "case_id": "FIR-2024-CYBER-809",\\n'
        '  "case_type": "Corporate Espionage & Data Leak",\\n'
        '  "victim_name": "State Defense Research Organization",\\n'
        '  "officer_name": "Inspector R. Vikram",\\n'
        '  "badge_id": "CB-TN-4091",\\n'
        '  "seizure_location": "Data Center Room B, Chennai",\\n'
        '  "latitude": 13.0827,\\n'
        '  "longitude": 80.2707,\\n'
        '  "original_filename": "cctv_server_room.mp4",\\n'
        '  "stored_filename": "1_cctv_server_room.mp4",\\n'
        '  "file_size_bytes": 10485760,\\n'
        '  "evidence_hash": "f793c5fd34c08961faceea698f8f9cd816dcb13132d2886912451d1323eb2706",\\n'
        '  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",\\n'
        '  "hmac_sig": "c95d92108d8465ce2fe73cd189c8e7abfe844426110d06b8186cc9c31067b0d9",\\n'
        '  "block_hash": "c55ae3a25ae01fc7621e8a0e766144d6e363c2c92b288a1edc9df5f443611fb4",\\n'
        '  "custody_trail": [\\n'
        "    {\\n"
        '      "step_no": 1,\\n'
        '      "challan_id": "CHL-2024-CYBER-809-T1",\\n'
        '      "from_entity": "Crime Scene / Seizure Site",\\n'
        '      "to_entity": "Inspector R. Vikram (CB-TN-4091)",\\n'
        '      "purpose": "Initial Seizure & Cryptographic Ingestion",\\n'
        '      "transferor_hmac": "e8910b...",\\n'
        '      "recipient_hmac": "f9021c...",\\n'
        '      "custody_status": "Evidence Locked in Vault"\\n'
        "    }\\n"
        "  ]\\n"
        "}"
    )
    p_schema = doc.add_paragraph()
    p_schema.paragraph_format.space_before = Pt(6)
    p_schema.paragraph_format.space_after = Pt(8)
    p_schema.paragraph_format.line_spacing = 1.15
    run_schema = p_schema.add_run(schema_snippet)
    run_schema.font.name = "Courier New"
    run_schema.font.size = Pt(9.5)
    run_schema.font.color.rgb = RGBColor(0, 102, 51)
'''

with open("generate_chapters_content.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace before REFERENCES
target = '    # =========================================================================\n    # REFERENCES / BIBLIOGRAPHY'
if target in content:
    new_content = content.replace(target, extra_code + '\n' + target)
    with open("generate_chapters_content.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully appended Appendix to generate_chapters_content.py")
else:
    print("Target not found in generate_chapters_content.py")
