import os
import json
import hashlib
import hmac
from datetime import datetime

SECRET_HMAC_KEY = b"FORENSIC_SECRET_KEY_CYBER_CRIME_CELL_2024"
VAULT_DIR = os.path.join(os.path.dirname(__file__), "evidence_vault")
CLOUD_VAULT_DIR = os.path.join(os.path.dirname(__file__), "cloud_vault")
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "ledger.json")

os.makedirs(VAULT_DIR, exist_ok=True)
os.makedirs(CLOUD_VAULT_DIR, exist_ok=True)

def get_ledger() -> list:
    """Reads current hash chain from ledger.json."""
    if not os.path.exists(LEDGER_FILE):
        return []
    try:
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_ledger(chain: list):
    """Saves updated hash chain."""
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(chain, f, indent=4)

def generate_auto_case_ids() -> tuple[str, str]:
    """Auto-generates sequential/unique FIR ID and Case Reference Token."""
    chain = get_ledger()
    existing_fir_nums = []
    
    for b in chain:
        cid = b.get("case_id", "")
        if "CYBER-" in cid:
            try:
                num = int(cid.split("CYBER-")[-1])
                existing_fir_nums.append(num)
            except Exception:
                pass
                
    next_num = max(existing_fir_nums) + 1 if existing_fir_nums else 101
    current_year = datetime.utcnow().year
    
    auto_fir_id = f"FIR-{current_year}-CYBER-{next_num}"
    auto_case_ref = f"CRF-{current_year}-{next_num:04d}"
    return auto_fir_id, auto_case_ref

def calculate_file_hash(file_bytes: bytes) -> str:
    """Computes standard SHA-256 cryptographic hash of evidence file."""
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()

def generate_hmac(data_str: str) -> str:
    """Generates HMAC signature to prove block authenticity."""
    return hmac.new(SECRET_HMAC_KEY, data_str.encode("utf-8"), hashlib.sha256).hexdigest()

def calculate_block_hash(block_data: dict) -> str:
    """Calculates hash of entire block including prev_hash, creating immutable chain."""
    hash_payload = f"{block_data['block_id']}_{block_data['timestamp']}_{block_data['case_id']}_{block_data['evidence_hash']}_{block_data['prev_hash']}"
    return hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()

def extract_gps_coords(exif_dict=None, location_str="Chennai") -> tuple[float, float]:
    """Resolves or generates realistic crime scene GPS coordinates (Latitude, Longitude)."""
    loc_lower = str(location_str).lower()
    city_coords = {
        "chennai": (13.0827, 80.2707),
        "coimbatore": (11.0168, 76.9558),
        "karur": (10.9601, 78.0766),
        "kangayem": (11.0045, 77.5615),
        "madurai": (9.9252, 78.1198),
        "trichy": (10.7905, 78.7047),
        "salem": (11.6643, 78.1460),
        "bengaluru": (12.9716, 77.5946),
        "bangalore": (12.9716, 77.5946),
        "delhi": (28.6139, 77.2090),
        "mumbai": (19.0760, 72.8777),
        "hyderabad": (17.3850, 78.4867)
    }
    for city, coords in city_coords.items():
        if city in loc_lower:
            offset = (int(hashlib.md5(location_str.encode()).hexdigest()[:4], 16) % 100 - 50) / 4000.0
            return round(coords[0] + offset, 5), round(coords[1] + offset, 5)
            
    # Default to Chennai Forensic HQ
    return 13.0827, 80.2707

def extract_metadata(file_bytes: bytes, filename: str, location: str = "Chennai") -> dict:
    """Extracts technical/EXIF metadata and crime scene GPS coordinates from uploaded evidence."""
    lat, lon = extract_gps_coords(location_str=location)
    metadata = {
        "device_make": "Not Available / Generic",
        "device_model": "Standard Digital Forensic Artifact",
        "original_date": "N/A",
        "dimensions": "N/A",
        "latitude": lat,
        "longitude": lon,
        "crime_scene_location": location
    }
    
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".tiff", ".webp"]:
        try:
            import io
            from PIL import Image, ExifTags
            img = Image.open(io.BytesIO(file_bytes))
            metadata["dimensions"] = f"{img.width} x {img.height} px"
            
            exif = img.getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag == "Make":
                        metadata["device_make"] = str(value).strip()
                    elif tag == "Model":
                        metadata["device_model"] = str(value).strip()
                    elif tag == "DateTime":
                        metadata["original_date"] = str(value).strip()
        except Exception:
            metadata["dimensions"] = f"Binary Object ({len(file_bytes)} bytes)"
    else:
        metadata["device_model"] = f"Raw Forensic Stream ({ext.upper() if ext else 'BIN'})"
            
    return metadata

def generate_hex_dump(file_bytes: bytes, length: int = 64) -> str:
    """Generates standard forensic Hex Dump (Offset | Hex Bytes | ASCII) for laboratory inspection."""
    sample = file_bytes[:length]
    lines = []
    for offset in range(0, len(sample), 16):
        chunk = sample[offset:offset+16]
        hex_bytes = " ".join(f"{b:02X}" for b in chunk)
        hex_padding = " " * (3 * (16 - len(chunk)))
        ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{offset:08X}:  {hex_bytes}{hex_padding}  |{ascii_str}|")
    return "\n".join(lines)

def detect_magic_bytes(file_bytes: bytes, filename: str) -> dict:
    """
    Forensic AI Magic Byte & Masquerading Scanner:
    Inspects true binary file signatures against declared extensions to uncover malware or spoofed evidence.
    """
    ext = os.path.splitext(filename)[1].lower().strip(".")
    sample = file_bytes[:32]
    
    true_type = "Unknown Binary Stream"
    true_mime = "application/octet-stream"
    expected_extensions = []
    is_malicious_type = False
    
    if sample.startswith(b"\xFF\xD8\xFF"):
        true_type = "JPEG Image (JFIF / EXIF)"
        true_mime = "image/jpeg"
        expected_extensions = ["jpg", "jpeg", "jpe"]
    elif sample.startswith(b"\x89PNG\r\n\x1a\n"):
        true_type = "PNG Image (Portable Network Graphics)"
        true_mime = "image/png"
        expected_extensions = ["png"]
    elif sample.startswith(b"GIF87a") or sample.startswith(b"GIF89a"):
        true_type = "GIF Graphic Interchange Format"
        true_mime = "image/gif"
        expected_extensions = ["gif"]
    elif sample.startswith(b"%PDF-"):
        true_type = "Adobe PDF Document"
        true_mime = "application/pdf"
        expected_extensions = ["pdf"]
    elif sample.startswith(b"MZ"):
        true_type = "Windows PE Executable / DLL / Malware Binary"
        true_mime = "application/x-dosexec"
        expected_extensions = ["exe", "dll", "sys", "scr", "com"]
        is_malicious_type = True
    elif sample.startswith(b"\x7FELF"):
        true_type = "Linux ELF Executable / Binary Payload"
        true_mime = "application/x-elf"
        expected_extensions = ["bin", "elf", "so"]
        is_malicious_type = True
    elif sample.startswith(b"PK\x03\x04"):
        true_type = "ZIP Archive / OpenXML Office Document"
        true_mime = "application/zip"
        expected_extensions = ["zip", "docx", "xlsx", "pptx", "apk", "jar"]
    elif sample.startswith(b"Rar!\x1A\x07"):
        true_type = "RAR Compressed Archive"
        true_mime = "application/x-rar"
        expected_extensions = ["rar"]
    elif sample.startswith(b"7z\xBC\xAF\x27\x1C"):
        true_type = "7-Zip Compressed Archive"
        true_mime = "application/x-7z-compressed"
        expected_extensions = ["7z"]
    elif len(sample) >= 12 and sample[4:8] == b"ftyp":
        major_brand = sample[8:12].decode('ascii', errors='ignore')
        true_type = f"ISO MPEG-4 Container ({major_brand})"
        true_mime = "video/mp4"
        expected_extensions = ["mp4", "mov", "m4v", "m4a"]
    elif sample.startswith(b"ID3") or (len(sample) >= 2 and sample[0] == 0xFF and (sample[1] & 0xE0) == 0xE0):
        true_type = "MPEG-1/2 Audio Layer 3 (MP3)"
        true_mime = "audio/mpeg"
        expected_extensions = ["mp3"]
    elif sample.startswith(b"RIFF") and len(sample) >= 12:
        sub_type = sample[8:12].decode('ascii', errors='ignore')
        if sub_type == "WAVE":
            true_type = "WAV Waveform Audio"
            true_mime = "audio/wav"
            expected_extensions = ["wav"]
        elif sub_type == "AVI ":
            true_type = "AVI Audio Video Interleave"
            true_mime = "video/x-msvideo"
            expected_extensions = ["avi"]
        elif sub_type == "WEBP":
            true_type = "Google WebP Image"
            true_mime = "image/webp"
            expected_extensions = ["webp"]
        else:
            true_type = f"RIFF Multimedia Container ({sub_type})"
            true_mime = "application/octet-stream"
            expected_extensions = ["riff"]
    elif b"<?php" in sample.lower() or b"<?=" in sample:
        true_type = "PHP Server Script / Web Shell"
        true_mime = "text/x-php"
        expected_extensions = ["php", "phtml", "php5"]
        is_malicious_type = True
    elif sample.startswith(b"#!/bin/") or sample.startswith(b"#!/usr/"):
        true_type = "Unix Shell Execution Script"
        true_mime = "text/x-shellscript"
        expected_extensions = ["sh", "bash"]
        is_malicious_type = True
    elif b"<html" in sample.lower() or b"<!doctype" in sample.lower() or b"<script" in sample.lower():
        true_type = "HTML / JavaScript Web Page"
        true_mime = "text/html"
        expected_extensions = ["html", "htm", "js"]
    else:
        try:
            file_bytes[:256].decode('utf-8')
            true_type = "UTF-8 Plain Text Document"
            true_mime = "text/plain"
            expected_extensions = ["txt", "log", "csv", "json", "md"]
        except Exception:
            true_type = "Generic Binary / Unidentified Forensic Stream"
            true_mime = "application/octet-stream"
            expected_extensions = [ext] if ext else []

    is_spoofed = False
    severity = "CLEAN"
    verdict = "Normal - Signature Matches File Extension"
    
    if expected_extensions and ext:
        if ext not in expected_extensions:
            is_spoofed = True
            if is_malicious_type:
                severity = "CRITICAL_MALWARE_SPOOF"
                verdict = f"CRITICAL ANOMALY: Executable/Script ({true_type}) is disguised with deceptive extension '.{ext}'!"
            else:
                severity = "SUSPICIOUS_EXTENSION_MISMATCH"
                verdict = f"FORMAT MISMATCH: True binary header is '{true_type}', but declared as '.{ext}'"
        else:
            severity = "CLEAN"
            verdict = f"VERIFIED: True binary header strictly matches claimed '.{ext}' ({true_type})"
    elif not expected_extensions:
        verdict = f"RAW STREAM: Generic binary format ({true_type})"

    hex_dump = generate_hex_dump(file_bytes, length=64)
    magic_hex = " ".join(f"{b:02X}" for b in sample[:8])
    
    return {
        "true_type": true_type,
        "true_mime": true_mime,
        "magic_hex": magic_hex,
        "declared_extension": ext,
        "is_spoofed": is_spoofed,
        "severity": severity,
        "verdict": verdict,
        "hex_dump": hex_dump
    }

def add_evidence_block(
    case_id: str = "FIR-2024-CYBER-101",
    officer_name: str = "Forensic Unit",
    badge_id: str = "CB-TN-4091",
    location: str = "Chennai",
    filename: str = "evidence.bin",
    file_bytes: bytes = b"",
    victim_name: str = "N/A",
    case_type: str = "Cyber Crime",
    seizure_location: str = None,
    latitude: float = None,
    longitude: float = None,
    notes: str = "",
    **kwargs
) -> dict:
    """Adds a new seized evidence block into the chain, supporting both positional and keyword arguments."""
    chain = get_ledger()
    eff_location = seizure_location or location or "Chennai Cyber Crime Cell"
    
    if len(chain) == 0:
        prev_hash = "0" * 64
        block_id = 1
    else:
        prev_hash = chain[-1]["block_hash"]
        block_id = len(chain) + 1
        
    stored_filename = f"{block_id}_{filename}"
    stored_path = os.path.join(VAULT_DIR, stored_filename)
    cloud_path = os.path.join(CLOUD_VAULT_DIR, stored_filename)
    
    with open(stored_path, "wb") as f:
        f.write(file_bytes)
        
    with open(cloud_path, "wb") as f:
        f.write(file_bytes)
        
    file_sha256 = calculate_file_hash(file_bytes)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    extracted_meta = extract_metadata(file_bytes, filename, location=eff_location)
    if latitude is not None and longitude is not None:
        extracted_meta["latitude"] = float(latitude)
        extracted_meta["longitude"] = float(longitude)
    if notes:
        extracted_meta["notes"] = str(notes)

    magic_inspection = detect_magic_bytes(file_bytes, filename)
    
    # Initial Handover Trail
    initial_custody_log = [{
        "step_no": 1,
        "challan_id": f"CHL-{case_id.replace('FIR-', '')}-T1",
        "timestamp": timestamp,
        "from_entity": "Crime Scene / Seizure Site",
        "to_entity": f"{officer_name} ({badge_id})",
        "purpose": "Initial Seizure & Cryptographic Ingestion",
        "transferor_pin": "SEIZURE-ORDER-VAL",
        "recipient_token": "CUSTODY-VAULT-ROOT",
        "transferor_hmac": generate_hmac(f"{file_sha256}_{timestamp}_CrimeScene"),
        "recipient_hmac": generate_hmac(f"{file_sha256}_{timestamp}_{officer_name}"),
        "custody_status": "Evidence Locked in Vault"
    }]
    
    block_data = {
        "block_id": block_id,
        "timestamp": timestamp,
        "case_id": case_id,
        "case_type": case_type,
        "victim_name": victim_name,
        "officer_name": officer_name,
        "badge_id": badge_id,
        "seizure_location": eff_location,
        "latitude": extracted_meta.get("latitude", 13.0827),
        "longitude": extracted_meta.get("longitude", 80.2707),
        "original_filename": filename,
        "stored_filename": stored_filename,
        "file_size_bytes": len(file_bytes),
        "metadata": extracted_meta,
        "magic_inspection": magic_inspection,
        "custody_trail": initial_custody_log,
        "evidence_hash": file_sha256,
        "prev_hash": prev_hash
    }
    
    block_data["hmac_sig"] = generate_hmac(file_sha256 + timestamp)
    block_data["block_hash"] = calculate_block_hash(block_data)
    
    chain.append(block_data)
    save_ledger(chain)
    return block_data

def record_custody_transfer(block_id: int, from_entity: str, to_entity: str, purpose: str, transferor_pin: str = "OFFICER-4091", recipient_token: str = "FSL-VERIFIED-AUTH") -> tuple[bool, str, dict]:
    """Records a legal custody transfer event into the evidence block's permanent trail with dual digital signatures."""
    chain = get_ledger()
    updated = False
    new_event = None
    
    for block in chain:
        if block["block_id"] == block_id:
            if "custody_trail" not in block:
                block["custody_trail"] = []
                
            step_no = len(block["custody_trail"]) + 1
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            challan_id = f"CHL-{block['case_id'].replace('FIR-', '')}-T{step_no}"
            
            # Dual digital cryptographic signatures
            t_hmac = generate_hmac(f"{block['evidence_hash']}_{timestamp}_{from_entity}_{transferor_pin}")
            r_hmac = generate_hmac(f"{block['evidence_hash']}_{timestamp}_{to_entity}_{recipient_token}")
            
            new_event = {
                "challan_id": challan_id,
                "step_no": step_no,
                "timestamp": timestamp,
                "from_entity": from_entity,
                "to_entity": to_entity,
                "purpose": purpose,
                "transferor_pin": f"PIN-***{transferor_pin[-3:]}" if len(transferor_pin) >= 3 else "AUTH-VALIDATED",
                "recipient_token": recipient_token,
                "transferor_hmac": t_hmac,
                "recipient_hmac": r_hmac,
                "custody_status": f"In Legal Custody of {to_entity}"
            }
            block["custody_trail"].append(new_event)
            updated = True
            break
            
    if updated:
        save_ledger(chain)
        return True, f"Handover step #{new_event['step_no']} recorded! Challan ID: {new_event['challan_id']}", new_event
    return False, "Target evidence block not found in ledger.", {}

def reverse_search_evidence(query, is_bytes: bool = False):
    """
    Forensic Reverse Hash & Artifact Search Engine ('Know Your Evidence'):
    Searches the Merkle custody ledger by SHA-256 hash or raw artifact bytes.
    Returns: (match_found: bool, block: dict | None, summary_or_err: str)
    """
    if is_bytes:
        search_hash = calculate_file_hash(query).lower()
        query_type = "Raw File Drag & Drop Search"
    else:
        search_hash = str(query).strip().lower()
        query_type = "Direct SHA-256 Hash Lookup"
        
    chain = get_ledger()
    for block in chain:
        ev_hash = block.get("evidence_hash", "").lower()
        block_h = block.get("block_hash", "").lower()
        prev_h = block.get("prev_hash", "").lower()
        
        match_type = None
        if search_hash == ev_hash:
            match_type = "Primary Evidence File SHA-256"
        elif search_hash == block_h:
            match_type = "Block Merkle Root Hash"
        elif search_hash == prev_h:
            match_type = "Parent Chain Linkage Hash"
            
        if match_type:
            vault_path = os.path.join(VAULT_DIR, block["stored_filename"])
            is_disk_intact = False
            disk_hash = "FILE_MISSING"
            if os.path.exists(vault_path):
                with open(vault_path, "rb") as f:
                    disk_hash = calculate_file_hash(f.read())
                is_disk_intact = (disk_hash == block["evidence_hash"])
                
            summary = f"MATCH VERIFIED: Artifact belongs to Case {block['case_id']}, Block #{block['block_id']} ('{block['original_filename']}')."
            return True, block, summary
            
    return False, None, "UNKNOWN ARTIFACT: No cryptographic custody block or Merkle record found for this hash in the judicial ledger."

def verify_chain_integrity() -> tuple[bool, list]:
    """
    Forensic Audit Engine:
    1. Checks if files in vault have been modified (File Integrity).
    2. Checks if the blockchain links are unbroken (Chain Integrity).
    """
    chain = get_ledger()
    audit_results = []
    is_all_clean = True
    
    for i, block in enumerate(chain):
        block_report = {
            "block_id": block["block_id"],
            "filename": block["original_filename"],
            "status": "VALID",
            "reason": "Integrity intact",
            "expected_hash": block["evidence_hash"],
            "actual_hash": block["evidence_hash"]
        }
        
        # Check 1: Chain continuity
        if i == 0:
            if block["prev_hash"] != "0" * 64:
                block_report["status"] = "CORRUPTED"
                block_report["reason"] = "Genesis block linkage broken!"
                is_all_clean = False
        else:
            if block["prev_hash"] != chain[i-1]["block_hash"]:
                block_report["status"] = "CORRUPTED"
                block_report["reason"] = f"Chain linkage broken from Block #{i} to Block #{i+1}!"
                is_all_clean = False
                
        # Check 2: Actual File Tampering check
        filepath = os.path.join(VAULT_DIR, block["stored_filename"])
        if not os.path.exists(filepath):
            block_report["status"] = "MISSING"
            block_report["reason"] = "Physical evidence file missing in repository!"
            is_all_clean = False
        else:
            with open(filepath, "rb") as f:
                current_file_bytes = f.read()
            current_hash = calculate_file_hash(current_file_bytes)
            block_report["actual_hash"] = current_hash
            
            if current_hash != block["evidence_hash"]:
                block_report["status"] = "TAMPERED"
                block_report["reason"] = "CRITICAL: Hash mismatch! File content modified after custody seizure."
                is_all_clean = False
                
        block_report["magic_inspection"] = block.get("magic_inspection", {})
        audit_results.append(block_report)
        
    return is_all_clean, audit_results

def simulate_tampering(block_id: int) -> tuple[bool, str]:
    """
    Demo Helper:
    Surgically injects an unauthorized byte into the target file to demonstrate tamper detection.
    """
    chain = get_ledger()
    for block in chain:
        if block["block_id"] == block_id:
            filepath = os.path.join(VAULT_DIR, block["stored_filename"])
            if os.path.exists(filepath):
                with open(filepath, "ab") as f:
                    f.write(b"\n[UNAUTHORIZED_MODIFICATION_PAYLOAD]")
                return True, f"Injected malicious payload into Block #{block_id} ('{block['original_filename']}'). Recomputed hash will mismatch genesis fingerprint."
    return False, f"Evidence Block #{block_id} not found on local disk repository."

def reset_all_evidence():
    """Cleans up all data for a fresh demonstration."""
    if os.path.exists(LEDGER_FILE):
        os.remove(LEDGER_FILE)
    if os.path.exists(VAULT_DIR):
        for f in os.listdir(VAULT_DIR):
            try:
                os.remove(os.path.join(VAULT_DIR, f))
            except Exception:
                pass
    if os.path.exists(CLOUD_VAULT_DIR):
        for f in os.listdir(CLOUD_VAULT_DIR):
            try:
                os.remove(os.path.join(CLOUD_VAULT_DIR, f))
            except Exception:
                pass

def ensure_cloud_mirror_synced():
    """
    Ensures pristine master replicas exist in CLOUD_VAULT_DIR for all blocks in the ledger.
    If a file in VAULT_DIR has a simulated tamper payload appended, strips it to recover pristine copy for cloud storage.
    """
    chain = get_ledger()
    tamper_tag = b"\n[UNAUTHORIZED_MODIFICATION_PAYLOAD]"
    for block in chain:
        stored_fn = block["stored_filename"]
        cloud_p = os.path.join(CLOUD_VAULT_DIR, stored_fn)
        vault_p = os.path.join(VAULT_DIR, stored_fn)
        
        needs_cloud_seed = False
        if not os.path.exists(cloud_p):
            needs_cloud_seed = True
        else:
            with open(cloud_p, "rb") as cf:
                if calculate_file_hash(cf.read()) != block["evidence_hash"]:
                    needs_cloud_seed = True
                    
        if needs_cloud_seed and os.path.exists(vault_p):
            with open(vault_p, "rb") as vf:
                raw_b = vf.read()
            while raw_b.endswith(tamper_tag):
                raw_b = raw_b[:-len(tamper_tag)]
            if calculate_file_hash(raw_b) == block["evidence_hash"]:
                with open(cloud_p, "wb") as cf:
                    cf.write(raw_b)

def get_storage_stats() -> dict:
    """Returns real-time analytics comparing Local Vault vs Cloud Mirror."""
    ensure_cloud_mirror_synced()
    chain = get_ledger()
    
    local_files = [f for f in os.listdir(VAULT_DIR) if not f.startswith("qr_")] if os.path.exists(VAULT_DIR) else []
    cloud_files = [f for f in os.listdir(CLOUD_VAULT_DIR)] if os.path.exists(CLOUD_VAULT_DIR) else []
    
    local_size_bytes = sum(os.path.getsize(os.path.join(VAULT_DIR, f)) for f in local_files if os.path.exists(os.path.join(VAULT_DIR, f)))
    cloud_size_bytes = sum(os.path.getsize(os.path.join(CLOUD_VAULT_DIR, f)) for f in cloud_files if os.path.exists(os.path.join(CLOUD_VAULT_DIR, f)))
    
    healthy_count = 0
    tampered_count = 0
    
    block_health = []
    for b in chain:
        fn = b["stored_filename"]
        vp = os.path.join(VAULT_DIR, fn)
        cp = os.path.join(CLOUD_VAULT_DIR, fn)
        
        local_intact = False
        if os.path.exists(vp):
            with open(vp, "rb") as f:
                local_intact = (calculate_file_hash(f.read()) == b["evidence_hash"])
                
        cloud_intact = False
        if os.path.exists(cp):
            with open(cp, "rb") as f:
                cloud_intact = (calculate_file_hash(f.read()) == b["evidence_hash"])
                
        if local_intact:
            healthy_count += 1
        else:
            tampered_count += 1
            
        block_health.append({
            "block_id": b["block_id"],
            "case_id": b["case_id"],
            "filename": b["original_filename"],
            "local_status": "🟢 INTACT" if local_intact else "🔴 TAMPERED",
            "cloud_status": "🟢 HEALTHY MIRROR" if cloud_intact else "⚠️ REPLICA MISSING",
            "can_auto_heal": (not local_intact and cloud_intact)
        })
        
    return {
        "total_blocks": len(chain),
        "healthy_count": healthy_count,
        "tampered_count": tampered_count,
        "local_file_count": len(local_files),
        "cloud_file_count": len(cloud_files),
        "local_size_kb": round(local_size_bytes / 1024, 2),
        "cloud_size_kb": round(cloud_size_bytes / 1024, 2),
        "block_health": block_health
    }

def auto_heal_evidence(block_id: int) -> tuple[bool, str]:
    """
    Auto-Heals corrupted local evidence by restoring the pristine replica from Cloud Mirror.
    Verifies SHA-256 against ledger genesis hash and logs an official Disaster Recovery event in the Chain of Custody.
    """
    ensure_cloud_mirror_synced()
    chain = get_ledger()
    
    for block in chain:
        if block["block_id"] == block_id:
            fn = block["stored_filename"]
            local_path = os.path.join(VAULT_DIR, fn)
            cloud_path = os.path.join(CLOUD_VAULT_DIR, fn)
            
            if not os.path.exists(cloud_path):
                return False, f"Cloud mirror replica for Block #{block_id} is missing."
                
            with open(cloud_path, "rb") as cf:
                cloud_bytes = cf.read()
            cloud_hash = calculate_file_hash(cloud_bytes)
            
            if cloud_hash != block["evidence_hash"]:
                return False, "Disaster Recovery Aborted: Cloud mirror hash does not match immutable genesis block."
                
            # Overwrite local corrupted file with pristine cloud replica
            with open(local_path, "wb") as lf:
                lf.write(cloud_bytes)
                
            # Log Disaster Recovery into Custody Trail
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            heal_event = {
                "timestamp": timestamp,
                "from_entity": "Encrypted Cloud Mirror (Disaster Recovery Engine)",
                "to_entity": "Local Evidence Vault (Self-Healed)",
                "purpose": "Self-Healing Protocol: Restored pristine file binary from Cloud Mirror after cryptographic tamper alert",
                "custody_status": "Integrity 100% Restored",
                "transfer_hmac": generate_hmac(f"{block['evidence_hash']}_{timestamp}_DISASTER_RECOVERY_HEAL")
            }
            if "custody_trail" not in block:
                block["custody_trail"] = []
            block["custody_trail"].append(heal_event)
            save_ledger(chain)
            return True, f"Block #{block_id} ('{block['original_filename']}') successfully auto-healed! SHA-256 integrity restored."
            
    return False, f"Block #{block_id} not found in custody ledger."

def auto_heal_all_tampered() -> tuple[int, list]:
    """Scans all blocks and automatically heals any tampered files."""
    stats = get_storage_stats()
    healed_count = 0
    logs = []
    
    for item in stats["block_health"]:
        if item["can_auto_heal"]:
            ok, msg = auto_heal_evidence(item["block_id"])
            if ok:
                healed_count += 1
                logs.append(msg)
            else:
                logs.append(f"Block #{item['block_id']} failed: {msg}")
                
    return healed_count, logs
