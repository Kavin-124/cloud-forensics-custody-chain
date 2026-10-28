import re

with open("generate_chapters_content.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace code_snippet block
old_code_pattern = re.compile(r'code_snippet\s*=\s*(?:r?""".*?"""|\(.*?\))\s*\n\s*p_code', re.DOTALL)

clean_code = '''code_snippet = (
        "import hashlib\\n"
        "import hmac\\n"
        "import json\\n"
        "import os\\n"
        "from datetime import datetime\\n\\n"
        "SECRET_HMAC_KEY = b\\"FORENSIC_SECRET_KEY_CYBER_CRIME_CELL_2024\\"\\n"
        "VAULT_DIR = \\"evidence_vault\\"\\n"
        "CLOUD_VAULT_DIR = \\"cloud_vault\\"\\n"
        "LEDGER_FILE = \\"ledger.json\\"\\n\\n"
        "def calculate_file_hash(file_bytes: bytes) -> str:\\n"
        "    sha256 = hashlib.sha256()\\n"
        "    sha256.update(file_bytes)\\n"
        "    return sha256.hexdigest()\\n\\n"
        "def generate_hmac(data_str: str) -> str:\\n"
        "    return hmac.new(SECRET_HMAC_KEY, data_str.encode(\\'utf-8\\'), hashlib.sha256).hexdigest()\\n\\n"
        "def calculate_block_hash(block_data: dict) -> str:\\n"
        "    payload = f\\\"{block_data[\\'block_id\\']}_{block_data[\\'timestamp\\']}_{block_data[\\'case_id\\']}_{block_data[\\'evidence_hash\\']}_{block_data[\\'prev_hash\\']}\\\"\\n"
        "    return hashlib.sha256(payload.encode(\\'utf-8\\')).hexdigest()\\n\\n"
        "def detect_magic_bytes(file_bytes: bytes, filename: str) -> dict:\\n"
        "    ext = os.path.splitext(filename)[1].lower().strip(\\'.\\')\\n"
        "    sample = file_bytes[:32]\\n"
        "    if sample.startswith(b\\'\\\\xff\\\\xd8\\\\xff\\'):\\n"
        "        true_type, expected = \\'JPEG Image (JFIF / EXIF)\\', [\\'jpg\\', \\'jpeg\\']\\n"
        "    elif sample.startswith(b\\'\\\\x89PNG\\\\r\\\\n\\\\x1a\\\\n\\'):\\n"
        "        true_type, expected = \\'PNG Image\\', [\\'png\\']\\n"
        "    elif sample.startswith(b\\'%PDF-\\'):\\n"
        "        true_type, expected = \\'PDF Document\\', [\\'pdf\\']\\n"
        "    elif sample.startswith(b\\'MZ\\'):\\n"
        "        true_type, expected = \\'Windows PE Executable / Malware Binary\\', [\\'exe\\', \\'dll\\']\\n"
        "    elif sample.startswith(b\\'\\\\x7fELF\\'):\\n"
        "        true_type, expected = \\'Linux ELF Binary Payload\\', [\\'elf\\', \\'bin\\']\\n"
        "    is_spoofed = (ext not in expected) if expected and ext else False\\n"
        "    return {\\'true_type\\': true_type, \\'is_spoofed\\': is_spoofed}\\n"
    )
    p_code'''

text = old_code_pattern.sub(clean_code, text)

with open("generate_chapters_content.py", "w", encoding="utf-8") as f:
    f.write(text)

print("generate_chapters_content.py patched successfully!")
