with open('generate_chapters_content.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip().startswith('code_snippet = ('):
        skip = True
        new_lines.append('    code_snippet = r"""import hashlib\n')
        new_lines.append('import hmac\n')
        new_lines.append('import json\n')
        new_lines.append('import os\n')
        new_lines.append('from datetime import datetime\n\n')
        new_lines.append('SECRET_HMAC_KEY = b"FORENSIC_SECRET_KEY_CYBER_CRIME_CELL_2024"\n')
        new_lines.append('VAULT_DIR = "evidence_vault"\n')
        new_lines.append('CLOUD_VAULT_DIR = "cloud_vault"\n')
        new_lines.append('LEDGER_FILE = "ledger.json"\n\n')
        new_lines.append('def calculate_file_hash(file_bytes: bytes) -> str:\n')
        new_lines.append('    sha256 = hashlib.sha256()\n')
        new_lines.append('    sha256.update(file_bytes)\n')
        new_lines.append('    return sha256.hexdigest()\n\n')
        new_lines.append('def generate_hmac(data_str: str) -> str:\n')
        new_lines.append('    return hmac.new(SECRET_HMAC_KEY, data_str.encode("utf-8"), hashlib.sha256).hexdigest()\n\n')
        new_lines.append('def calculate_block_hash(block_data: dict) -> str:\n')
        new_lines.append('    payload = f"{block_data[\'block_id\']}_{block_data[\'timestamp\']}_{block_data[\'case_id\']}_{block_data[\'evidence_hash\']}_{block_data[\'prev_hash\']}"\n')
        new_lines.append('    return hashlib.sha256(payload.encode("utf-8")).hexdigest()\n\n')
        new_lines.append('def detect_magic_bytes(file_bytes: bytes, filename: str) -> dict:\n')
        new_lines.append('    ext = os.path.splitext(filename)[1].lower().strip(".")\n')
        new_lines.append('    sample = file_bytes[:32]\n')
        new_lines.append('    if sample.startswith(b"\\xFF\\xD8\\xFF"):\n')
        new_lines.append('        true_type, expected = "JPEG Image (JFIF / EXIF)", ["jpg", "jpeg"]\n')
        new_lines.append('    elif sample.startswith(b"\\x89PNG\\r\\n\\x1a\\n"):\n')
        new_lines.append('        true_type, expected = "PNG Image", ["png"]\n')
        new_lines.append('    elif sample.startswith(b"%PDF-"):\n')
        new_lines.append('        true_type, expected = "PDF Document", ["pdf"]\n')
        new_lines.append('    elif sample.startswith(b"MZ"):\n')
        new_lines.append('        true_type, expected = "Windows PE Executable / Malware Binary", ["exe", "dll"]\n')
        new_lines.append('    elif sample.startswith(b"\\x7FELF"):\n')
        new_lines.append('        true_type, expected = "Linux ELF Binary Payload", ["elf", "bin"]\n')
        new_lines.append('    is_spoofed = (ext not in expected) if expected and ext else False\n')
        new_lines.append('    return {"true_type": true_type, "is_spoofed": is_spoofed}"""\n')
        continue
    if skip and line.strip().startswith('p_code = doc.add_paragraph()'):
        skip = False

    if line.strip().startswith('schema_snippet = ('):
        skip = True
        new_lines.append('    schema_snippet = """{\n')
        new_lines.append('  "block_id": 1,\n')
        new_lines.append('  "timestamp": "2026-10-20 04:07:42 UTC",\n')
        new_lines.append('  "case_id": "FIR-2024-CYBER-809",\n')
        new_lines.append('  "case_type": "Corporate Espionage & Data Leak",\n')
        new_lines.append('  "victim_name": "State Defense Research Organization",\n')
        new_lines.append('  "officer_name": "Inspector R. Vikram",\n')
        new_lines.append('  "badge_id": "CB-TN-4091",\n')
        new_lines.append('  "seizure_location": "Data Center Room B, Chennai",\n')
        new_lines.append('  "latitude": 13.0827,\n')
        new_lines.append('  "longitude": 80.2707,\n')
        new_lines.append('  "original_filename": "cctv_server_room.mp4",\n')
        new_lines.append('  "stored_filename": "1_cctv_server_room.mp4",\n')
        new_lines.append('  "file_size_bytes": 10485760,\n')
        new_lines.append('  "evidence_hash": "f793c5fd34c08961faceea698f8f9cd816dcb13132d2886912451d1323eb2706",\n')
        new_lines.append('  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",\n')
        new_lines.append('  "hmac_sig": "c95d92108d8465ce2fe73cd189c8e7abfe844426110d06b8186cc9c31067b0d9",\n')
        new_lines.append('  "block_hash": "c55ae3a25ae01fc7621e8a0e766144d6e363c2c92b288a1edc9df5f443611fb4",\n')
        new_lines.append('  "custody_trail": [\n')
        new_lines.append('    {\n')
        new_lines.append('      "step_no": 1,\n')
        new_lines.append('      "challan_id": "CHL-2024-CYBER-809-T1",\n')
        new_lines.append('      "from_entity": "Crime Scene / Seizure Site",\n')
        new_lines.append('      "to_entity": "Inspector R. Vikram (CB-TN-4091)",\n')
        new_lines.append('      "purpose": "Initial Seizure & Cryptographic Ingestion",\n')
        new_lines.append('      "transferor_hmac": "e8910b...",\n')
        new_lines.append('      "recipient_hmac": "f9021c...",\n')
        new_lines.append('      "custody_status": "Evidence Locked in Vault"\n')
        new_lines.append('    }\n')
        new_lines.append('  ]\n')
        new_lines.append('}"""\n')
        continue
    if skip and line.strip().startswith('p_schema = doc.add_paragraph()'):
        skip = False

    if not skip:
        new_lines.append(line)

with open('generate_chapters_content.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("generate_chapters_content.py successfully rewritten!")
