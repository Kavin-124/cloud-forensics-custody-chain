# Cryptographic Chain of Custody System for Digital Forensics in Cloud Environments

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/frontend-Streamlit%201.35+-FF4B4B.svg)](https://streamlit.io/)
[![Compliance](https://img.shields.io/badge/compliance-BSA%202023%20§63%20|%20IEA%20§65B-059669.svg)](#statutory-compliance)
[![License](https://img.shields.io/badge/license-MIT-slate.svg)](LICENSE)

An enterprise-grade, tamper-evident cryptographic digital forensics evidence ledger and chain of custody management platform. Built to satisfy statutory admissibility requirements under **Section 63 of the Bharatiya Sakshya Adhiniyam (BSA) 2023** and **Section 65B of the Indian Evidence Act (IEA)**.

---

## 🏛️ System Architecture & Four-Tier Access Portals

The vault provides four isolated, role-segregated institutional terminals:

| Role / Portal | Jurisdiction / Function | Statutory Mandate |
| :--- | :--- | :--- |
| **Law Enforcement** (`police`) | Evidence Seizure, Bitstream Imaging (SHA-256), Geolocation Sealing, Custody Transfer Handover Challans | CrPC §102 / BNSS §105 Evidence Seizure |
| **Counsel & Bar** (`lawyer`) | Exhibit Discovery, Reverse Hash Verification, Evidentiary Objections, Section 65B Certificates | BSA 2023 §63 / IEA §65B Admissibility |
| **Judicial Bench** (`judge`) | Cryptographic Integrity Verification, Tamper-Evident Matrix, Judicial Admissibility Determinations | Final Bench Order & Court Seal |
| **Root Authority** (`admin`) | Cryptographic Identity Provisioning, Merkle Root Verification, Forensic Auto-Healing Engine | Custody Ledger Governance |

---

## 🔐 Key Technical Features

1. **Cryptographic Bitstream Hashing:**
   - Dual SHA-256 computation over binary bitstreams.
   - HMAC-SHA256 digital signature sealing for all custody transfer transactions.
   - Incremental Merkle root recalculation preventing post-seizure ledger mutation.

2. **Self-Healing Forensic Ledger:**
   - Real-time tamper detection identifying bitstream corruption or metadata manipulation.
   - Cryptographic state snapshotting for disaster recovery and automated ledger self-healing.

3. **Statutory 65B Certificate Generation:**
   - Automated generation of court-admissible forensic audit certificates (`.pdf`) compliant with Indian Evidence Act Section 65B(4) and BSA 2023 Section 63.
   - Cryptographic QR codes embedded for offline judicial verification.

4. **Forensic Geolocation & Crime Scene Mapping:**
   - Seizure GPS coordinates validation and visualization.
   - Interactive evidence route telemetry mapping from seizure to forensic lab.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository & Install Dependencies
```bash
git clone https://github.com/<your-username>/cloud-forensics-custody.git
cd cloud-forensics-custody

# Create and activate virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Launch Platform
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📋 Evaluation Sandbox (Pre-Configured Accounts)

For academic evaluations and demonstrations, use the built-in **Institutional Sandbox** or manual credentials:

| Division | Identifier | Passphrase | Assigned Personnel |
| :--- | :--- | :--- | :--- |
| **Law Enforcement** | `CB-TN-4091` | `police123` | Insp. R. Vikram (Cyber Crime Wing) |
| **Legal Counsel** | `advocate_kavin` | `lawyer123` | Adv. Kavin R. (High Court Bar) |
| **Judicial Bench** | `justice_sharma` | `judge123` | Hon. Justice S. Sharma (Sessions Bench) |
| **Root Admin** | `admin` | `admin123` | Chief Forensic Registrar (Cloud Node) |

---

## 📁 Repository Structure

```
├── app.py                     # Main application entry point & role router
├── crypto_chain.py            # Core cryptographic blockchain & Merkle custody ledger
├── pdf_generator.py           # Forensic Section 65B & Handover challan PDF engine
├── requirements.txt           # Python library dependencies
├── backend/
│   ├── auth_service.py        # RBAC identity authentication & session management
│   └── audit_service.py       # Tamper detection telemetry & system audit logger
├── ui/
│   ├── theme.py               # Enterprise sovereign design system & typography
│   ├── login_page.py          # Institutional authentication gateway
│   ├── police_portal.py       # Evidence intake & chain of custody handover terminal
│   ├── lawyer_portal.py       # Evidentiary discovery, reverse hash search & 65B terminal
│   ├── judge_portal.py        # Judicial determinations & cryptographic audit bench
│   └── admin_portal.py        # Ledger governance, auto-healing & identity provisioning
├── static/
│   └── fonts/                 # Clean font binaries served via static server
└── .streamlit/
    └── config.toml            # Server settings & static file hosting configuration
```

---

## ⚖️ Statutory Compliance

- **Bharatiya Sakshya Adhiniyam (BSA) 2023, Section 63** — Conditions for admissibility of electronic records.
- **Indian Evidence Act (IEA) 1872, Section 65B** — Special provisions as to evidence relating to electronic record.
- **ISO/IEC 27037:2012** — Guidelines for identification, collection, acquisition, and preservation of digital evidence.

---

## 👨‍💻 Author & Academic Project
- Developed as a specialized **Digital Cloud Forensics & Cryptographic Custody Ledger System**.
- Affiliation: Department of Information Technology, V.S.B. Engineering College.
