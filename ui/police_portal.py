import streamlit as st
import os
from datetime import datetime
from crypto_chain import (
    get_ledger,
    add_evidence_block,
    detect_magic_bytes,
    record_custody_transfer,
    extract_gps_coords,
    VAULT_DIR,
    CLOUD_VAULT_DIR,
    auto_heal_evidence
)
from pdf_generator import generate_handover_challan_pdf, check_block_tampered
from backend.audit_service import log_event

def render_police_portal(user: dict):
    # Enterprise Command Header
    st.markdown(f"""
    <div class="enterprise-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="inst-badge police">Law Enforcement Directorate</span>
                    <span class="telemetry-beacon">
                        <span class="dot"></span> NODE ACTIVE // VERIFIED BY NIST SHA-256
                    </span>
                </div>
                <h1>Evidence Intake & Custody Terminal</h1>
                <p>Authorized Officer: <strong>{user.get('full_name')}</strong> | Service Identifier: <code>{user.get('identifier')}</code> | Division: {user.get('department')}</p>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">
                STANDARD: ISO/IEC 27037<br/>
                STATUTE: BSA 2023 §63 / IEA §65B
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chain = get_ledger()
    officer_blocks = [b for b in chain if b.get("badge_id") == user.get("identifier") or b.get("officer_name") == user.get("full_name")]

    # Key Operational Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Seized Artifacts</div>
            <div class="metric-value">{len(officer_blocks)}</div>
            <div class="metric-sub">Across Registered FIR Dockets</div>
            """, unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            cases_count = len(set(b.get("case_id") for b in officer_blocks)) if officer_blocks else 0
            st.markdown(f"""
            <div class="metric-label">Active Investigations</div>
            <div class="metric-value">{cases_count}</div>
            <div class="metric-sub">Cyber Crime Division</div>
            """, unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Cloud Dual-Vault Mirror</div>
            <div class="metric-value" style="color: #059669;">Synchronized</div>
            <div class="metric-sub">Disaster Recovery Active</div>
            """, unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Statutory Compliance</div>
            <div class="metric-value">Section 65B</div>
            <div class="metric-sub">Indian Evidence Act / BSA 2023</div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Main Tabs
    pol_tab1, pol_tab2, pol_tab3, pol_tab4 = st.tabs([
        "Evidence Ingestion",
        "Custody Vault Ledger",
        "Inter-Agency Handover",
        "Crime Scene GIS"
    ])

    # ---------------- TAB 1: EVIDENCE INGESTION ----------------
    with pol_tab1:
        with st.container(border=True):
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 16px;">
                <div>
                    <h3 style="margin: 0; font-size: 17px; font-weight: 700; color: #0F172A;">1. Electronic Artifact Seizure & Merkle Ingestion</h3>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #64748B;">
                        Capture digital bitstreams, execute automated magic-byte verification, derive SHA-256 digests, and anchor into the immutable custody ledger.
                    </p>
                </div>
                <span class="inst-badge police">BSA 2023 §63 COMPLIANT</span>
            </div>
            """, unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Select Digital Evidence Artifact to Ingest:",
                type=None,
                help="Accepts all binary file extensions (.mp4, .png, .jpg, .pdf, .raw, .img, .pcap, .txt, .zip)"
            )

            # Live AI Magic-Byte Scanner Preview
            magic_info = None
            if uploaded_file is not None:
                file_bytes = uploaded_file.getvalue()
                magic_info = detect_magic_bytes(file_bytes, uploaded_file.name)

                if magic_info.get("is_spoofed"):
                    st.error(f"""
                    **Security Anomaly Detected: Binary Masquerade Alert**  
                    The declared file extension claims to be `.{uploaded_file.name.split('.')[-1]}` but the true binary header is:
                    **{magic_info.get('true_type')}**. This artifact exhibits Trojan masquerade characteristics.
                    """)
                else:
                    st.success(f"**Binary Signature Verified:** {magic_info.get('true_type')} (MIME alignment confirmed) | Header Hex: `{magic_info.get('magic_hex', 'N/A')}`")

            # Case Metadata Form
            col_fir, col_type = st.columns(2)
            with col_fir:
                case_id = st.text_input("FIR / Case Docket Reference", value=f"FIR-{datetime.utcnow().year}-CYBER-101")
            with col_type:
                case_type = st.selectbox(
                    "Offense Classification",
                    [
                        "Corporate Espionage & Data Exfiltration",
                        "Ransomware & Cyber Extortion",
                        "Financial Banking Fraud & Phishing",
                        "Unauthorized Server Access & Web Defacement",
                        "Critical Infrastructure Cyber Sabotage",
                        "Cryptocurrency Laundering"
                    ]
                )

            col_victim, col_loc = st.columns(2)
            with col_victim:
                victim_name = st.text_input("Complainant / Victim Entity", value="State Defense Research Org")
            with col_loc:
                location = st.selectbox(
                    "Crime Scene Jurisdiction",
                    ["Chennai", "Coimbatore", "Karur", "Madurai", "Tiruchirappalli", "Salem"]
                )

            seizure_notes = st.text_area("Seizure Protocol & Write-Blocker Affidavit", "Seized directly from crime scene server room. Hardware bitstream write-blocker attached prior to extraction.")

            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #2563EB; border-radius: 8px; padding: 12px 16px; margin: 10px 0 16px 0;">
                <div style="font-size: 11.5px; font-weight: 700; color: #0F172A; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 2px;">
                    Statutory Admissibility Affirmation (Section 65B(2) IEA & Section 63 BSA 2023)
                </div>
                <div style="font-size: 12px; color: #475569; line-height: 1.5;">
                    • Electronic record remained in continuous lawful custody • Hardware write-blocking procedures prevented bitstream alteration • Synchronous dual-vault storage eliminates single point of failure • Cryptographic hash chaining guarantees non-repudiation.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Commit Artifact to Merkle Chain →", type="primary", use_container_width=True):
                if uploaded_file is None:
                    st.warning("Please select an evidence file before committing to the ledger.")
                else:
                    with st.spinner("Computing NIST SHA-256 digest, deriving HMAC signature & synchronizing vault mirror..."):
                        lat, lon = extract_gps_coords(location_str=location)
                        new_block = add_evidence_block(
                            file_bytes=uploaded_file.getvalue(),
                            filename=uploaded_file.name,
                            case_id=case_id,
                            case_type=case_type,
                            victim_name=victim_name,
                            officer_name=user.get("full_name"),
                            badge_id=user.get("identifier"),
                            seizure_location=f"{location} Cyber Crime Cell",
                            latitude=lat,
                            longitude=lon,
                            notes=seizure_notes
                        )

                        log_event(
                            user.get("full_name"),
                            "POLICE",
                            "EVIDENCE_SEIZURE",
                            f"Seized '{uploaded_file.name}' for {case_id} (Block #{new_block['block_id']})"
                        )

                        st.session_state["recent_ingested_block"] = new_block
                        st.toast(f"Exhibit #{new_block['block_id']} permanently bound to Merkle Ledger!", icon="⚖️")
                        st.success(f"✅ Artifact Successfully Bound to Immutable Ledger as Block #{new_block['block_id']}!")
                        st.markdown(f"""
                        <div style="background: #F0FDF4; border: 1px solid #86EFAC; border-left: 4px solid #16A34A; border-radius: 8px; padding: 16px 20px; margin: 14px 0 16px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #DCFCE7; padding-bottom: 8px; margin-bottom: 12px;">
                                <div style="font-size: 14.5px; font-weight: 700; color: #166534;">
                                    Official Cryptographic Seizure Receipt // Merkle Block #{new_block['block_id']}
                                </div>
                                <span class="inst-badge admin">IMMUTABLE ANCHOR</span>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; font-size: 13px; color: #1E293B;">
                                <div><strong>Artifact Name:</strong> <code>{uploaded_file.name}</code> ({len(uploaded_file.getvalue()) / (1024*1024):.2f} MB)</div>
                                <div><strong>Case Reference:</strong> <code style="color: #2563EB;">{case_id}</code> ({case_type})</div>
                                <div><strong>Seizing Officer:</strong> {user.get('full_name')} (<code>{user.get('identifier')}</code>)</div>
                                <div><strong>Seizure Location:</strong> {location} Cyber Crime Cell</div>
                                <div style="grid-column: span 2;"><strong>NIST SHA-256 Digest:</strong> <code style="font-size: 12px; color: #0284C7;">{new_block['evidence_hash']}</code></div>
                                <div style="grid-column: span 2;"><strong>Dual-Vault Status:</strong> <span style="color: #059669; font-weight: 600;">✓ Synchronized to On-Premises Vault & Encrypted Cloud Mirror</span></div>
                            </div>
                            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #DCFCE7; font-size: 12.5px; color: #15803D;">
                                📌 <strong>Next Step:</strong> Switch to <strong>Tab 2 (Custody Vault Ledger)</strong> to inspect the exhibit block, or <strong>Tab 3 (Inter-Agency Handover)</strong> to execute a transfer challan!
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    # ---------------- TAB 2: SEIZED EVIDENCE LOCKER ----------------
    with pol_tab2:
        st.markdown("""
        <div class="forensic-card">
            <h3>2. Active Evidence Vault & Merkle Ledger</h3>
            <p>
                All digital exhibits retained under continuous cryptographic custody. Select any exhibit to review its SHA-256 fingerprint, custody trail, and storage verification.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.info("No electronic artifacts recorded in ledger. Ingest evidence in Tab 1.")
        else:
            # Check for any tampered artifacts on disk
            any_tampered = any(check_block_tampered(b)[0] for b in chain)
            if any_tampered:
                st.error("🚨 **CRITICAL FORENSIC INTEGRITY ALERT: Bitstream Mismatch Detected on Local Storage!** One or more exhibits fail SHA-256 verification against the immutable Merkle chain.")

            for b in reversed(chain):
                is_tampered, disk_hash = check_block_tampered(b)
                status_icon = "🚨 [TAMPER DETECTED]" if is_tampered else "✓"
                expander_label = f"{status_icon} Exhibit #{b['block_id']}: {b.get('original_filename')} — Case: {b.get('case_id')}"
                
                with st.expander(expander_label, expanded=is_tampered):
                    if is_tampered:
                        st.error(f"""
                        **CRITICAL INTEGRITY BREACH:** The physical file on disk has been modified post-seizure!
                        - **Genesis Seizure SHA-256:** `{b.get('evidence_hash')}`
                        - **Current Disk Recomputed SHA-256:** `{disk_hash}`
                        - **Legal Status:** INADMISSIBLE UNDER BSA 2023 §63 / IEA §65B
                        """)
                        col_heal_l, col_heal_r = st.columns([2, 1])
                        with col_heal_l:
                            st.info("The synchronized pristine replica in `cloud_vault/` is intact and can restore bitstream integrity.")
                        with col_heal_r:
                            if st.button(f"Self-Heal from Cloud Mirror ➔", key=f"heal_pol_{b['block_id']}", type="primary", use_container_width=True):
                                ok, msg = auto_heal_evidence(b["block_id"])
                                if ok:
                                    log_event(user.get("full_name"), "POLICE", "AUTO_HEAL", f"Restored Block #{b['block_id']} from Cloud Mirror")
                                    st.toast(f"Exhibit #{b['block_id']} successfully restored!", icon="✅")
                                    st.rerun()

                    c1, c2, c3 = st.columns([1.5, 1.5, 1])
                    with c1:
                        st.markdown(f"**Artifact Name:** `{b.get('original_filename')}`")
                        st.markdown(f"**Case Reference:** `{b.get('case_id')}` ({b.get('case_type')})")
                        st.markdown(f"**Seizing Officer:** {b.get('officer_name')} (`{b.get('badge_id')}`)")
                        st.markdown(f"**Seizure Location:** {b.get('seizure_location')}")
                    with c2:
                        st.markdown(f"**Timestamp (UTC):** `{b.get('timestamp')}`")
                        st.markdown(f"**NIST SHA-256 Genesis Hash:**")
                        st.code(b.get("evidence_hash"), language=None)
                        st.markdown(f"**HMAC Signature:**")
                        st.code(b.get("hmac_sig", "N/A"), language=None)
                    with c3:
                        st.markdown("**Storage Redundancy:**")
                        file_path = os.path.join(VAULT_DIR, b.get("stored_filename", ""))
                        if not os.path.exists(file_path):
                            st.markdown("<span style='font-size: 11px; font-weight: 600; color: #DC2626; background: #FEF2F2; padding: 3px 8px; border-radius: 4px; border: 1px solid #FECACA;'>LOCAL MISSING</span>", unsafe_allow_html=True)
                        elif is_tampered:
                            st.markdown("<span style='font-size: 11px; font-weight: 700; color: #DC2626; background: #FEF2F2; padding: 3px 8px; border-radius: 4px; border: 1px solid #FECACA; display: inline-block;'>🚨 TAMPERED</span>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='font-size: 11px; font-weight: 600; color: #059669; background: #ECFDF5; padding: 3px 8px; border-radius: 4px; border: 1px solid #A7F3D0;'>ON-PREM VAULT OK</span>", unsafe_allow_html=True)

                        cloud_path = os.path.join(CLOUD_VAULT_DIR, b.get("stored_filename", ""))
                        if os.path.exists(cloud_path):
                            st.markdown("<span style='font-size: 11px; font-weight: 600; color: #2563EB; background: #EFF6FF; padding: 3px 8px; border-radius: 4px; border: 1px solid #BFDBFE; display: inline-block; margin-top: 6px;'>CLOUD MIRROR OK</span>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='font-size: 11px; font-weight: 600; color: #D97706; background: #FFFBEB; padding: 3px 8px; border-radius: 4px; border: 1px solid #FDE68A; display: inline-block; margin-top: 6px;'>SYNC PENDING</span>", unsafe_allow_html=True)

    # ---------------- TAB 3: INTER-AGENCY CUSTODY HANDOVER ----------------
    with pol_tab3:
        st.markdown("""
        <div class="forensic-card">
            <h3>3. Inter-Agency Custodial Handover Protocol</h3>
            <p>
                Physical and logical transmission between Police ➔ Forensic Science Laboratory (FSL) ➔ Magistrate Court requires mutual non-repudiation.
                Both authorities sign with cryptographic tokens and generate a statutory <strong>Inter-Agency Custody Challan</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.warning("No evidence artifacts in ledger to transfer.")
        else:
            with st.container(border=True):
                block_options = {f"Exhibit #{b['block_id']}: {b.get('original_filename')} ({b.get('case_id')})": b['block_id'] for b in chain}
                sel_label = st.selectbox(
                    "Select Evidence Artifact to Hand Over:",
                    list(block_options.keys()),
                    key="police_handover_sel"
                )
                target_block_id = block_options[sel_label]
                target_block = next((b for b in chain if b["block_id"] == target_block_id), None)

                # Dynamic Exhibit & Case Metadata
                fir_no = target_block.get('case_id', 'N/A')
                seizing_officer = target_block.get('officer_name', user.get('full_name'))
                badge_id = target_block.get('badge_id', user.get('identifier'))
                seizure_loc = target_block.get('seizure_location', 'N/A')
                seizure_time = target_block.get('timestamp', 'N/A')
                case_type = target_block.get('case_type', 'Cyber Crime')

                # Determine current legal custodian from custody trail
                trail = target_block.get("custody_trail", [])
                if trail:
                    current_custodian = trail[-1].get("to_entity", f"{seizing_officer} ({badge_id})")
                    custody_badge = f"<span style='color: #2563EB; font-weight: 600;'>{current_custodian}</span>"
                else:
                    current_custodian = f"{seizing_officer} ({badge_id})"
                    custody_badge = f"<span style='color: #059669; font-weight: 600;'>Seizing Officer ({seizing_officer})</span>"

                # Dynamic Dossier Display Card
                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px 16px; margin: 10px 0 16px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 10px;">
                        <div style="font-size: 13.5px; font-weight: 700; color: #0F172A;">
                            Case Docket Reference: <span style="color: #2563EB; font-family: 'JetBrains Mono', monospace;">{fir_no}</span>
                            <span style="color: #64748B; font-weight: 400; margin-left: 8px; font-size: 12.5px;">({case_type})</span>
                        </div>
                        <span class="inst-badge police">Exhibit #{target_block_id}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; font-size: 12.5px;">
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block; margin-bottom: 2px;">Original Seizing Officer</span>
                            <strong style="color: #0F172A;">{seizing_officer}</strong> <code style="font-size: 11px;">{badge_id}</code>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block; margin-bottom: 2px;">Current Legal Custodian</span>
                            <div>{custody_badge}</div>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block; margin-bottom: 2px;">Crime Scene Location</span>
                            <span style="color: #0F172A;">{seizure_loc}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                is_target_tampered, curr_hash = check_block_tampered(target_block)
                if is_target_tampered:
                    st.error(f"""
                    🚨 **CRITICAL INTEGRITY BREACH: BITSTREAM TAMPERING DETECTED ON EXHIBIT #{target_block_id}!**  
                    - **Genesis Hash (Seizure):** `{target_block.get('evidence_hash')}`  
                    - **Live Disk Hash (Current):** `{curr_hash}`  
                    - **Legal Status:** **FLAGGED: COMPROMISED (INADMISSIBLE BSA 2023 §63 / IEA §65B)**  
                    *Any Handover Challan issued for this exhibit will embed a statutory Tamper Alert Banner and print the live corrupted hash.*
                    """)

                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.text_input(
                        "FIR / Case Docket Reference",
                        value=fir_no,
                        disabled=True,
                        key=f"handover_fir_{target_block_id}",
                        help="Directly mapped to the selected electronic artifact's FIR record"
                    )
                with col_f2:
                    from_entity = st.text_input(
                        "Transferor Authority / Releasing Officer",
                        value=current_custodian,
                        key=f"from_entity_{target_block_id}",
                        help="Current authority releasing custody under official protocol"
                    )

                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    to_entity = st.text_input(
                        "Recipient Agency / Department",
                        value="State Forensic Science Laboratory (FSL Chennai)",
                        key=f"to_entity_{target_block_id}"
                    )
                with col_h2:
                    transferor_pin = st.text_input(
                        "Transferor Digital PIN",
                        type="password",
                        value="9876",
                        key=f"transferor_pin_{target_block_id}",
                        help="Secret PIN of releasing officer to compute dual HMAC signatures"
                    )

                purpose = st.selectbox(
                    "Transfer Purpose",
                    [
                        "Forensic Bitstream Clone & Deleted File Recovery",
                        "Malware Extraction & Reverse Engineering",
                        "Court Presentation & Evidence Box Deposit",
                        "Defense Counsel Discovery Inspection",
                        "Judicial Sealed Vault Deposit"
                    ],
                    key=f"purpose_{target_block_id}"
                )

                if st.button("Execute Custodial Handover & Issue Challan", type="primary", use_container_width=True, key=f"btn_handover_{target_block_id}"):
                    success, msg, new_step = record_custody_transfer(
                        target_block_id,
                        from_entity=from_entity,
                        to_entity=to_entity,
                        purpose=purpose,
                        transferor_pin=transferor_pin,
                        recipient_token="FSL-RECV-KEY-2024"
                    )
                    if success:
                        log_event(user.get("full_name"), "POLICE", "CUSTODY_HANDOVER", f"Transferred Block #{target_block_id} to {to_entity}")
                        st.success(f"Custody Step #{new_step['step_no']} registered. Challan ID: `{new_step['challan_id']}`")

                        # Generate and allow download of Challan PDF
                        target_block = next(b for b in get_ledger() if b["block_id"] == target_block_id)
                        challan_bytes = generate_handover_challan_pdf(target_block, new_step)
                        st.download_button(
                            label="Download Official Custody Transfer Challan (PDF)",
                            data=challan_bytes,
                            file_name=f"Handover_Challan_{new_step['challan_id']}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key=f"btn_dl_challan_{target_block_id}"
                        )
                    else:
                        st.error(msg)

                # Prior custody chain trail inspection
                if trail:
                    with st.expander(f"Prior Custodial Steps for Exhibit #{target_block_id} ({len(trail)} Events)", expanded=True if is_target_tampered else False):
                        for step in reversed(trail):
                            col_s1, col_s2 = st.columns([3, 1])
                            with col_s1:
                                st.markdown(f"**Step #{step.get('step_no')}** (`{step.get('timestamp')}`): `{step.get('from_entity')}` ➔ `{step.get('to_entity')}` | *{step.get('purpose')}* | Challan: `{step.get('challan_id')}`")
                            with col_s2:
                                past_pdf = generate_handover_challan_pdf(target_block, step)
                                st.download_button(
                                    label=f"📄 Download Challan #{step.get('step_no')}",
                                    data=past_pdf,
                                    file_name=f"Handover_Challan_{step.get('challan_id')}.pdf",
                                    mime="application/pdf",
                                    key=f"dl_past_chl_{target_block_id}_{step.get('step_no')}",
                                    use_container_width=True
                                )

    # ---------------- TAB 4: CRIME SCENE GEOLOCATION ----------------
    with pol_tab4:
        st.markdown("""
        <div class="forensic-card">
            <h3>4. Crime Scene Forensic Geolocation Telemetry</h3>
            <p>
                Spatial coordinates and crime scene jurisdiction logged during digital artifact seizure, plotted on the GIS map layer.
            </p>
        </div>
        """, unsafe_allow_html=True)

        geo_data = []
        for b in chain:
            lat = b.get("latitude")
            lon = b.get("longitude")
            if lat and lon:
                geo_data.append({
                    "lat": float(lat),
                    "lon": float(lon),
                    "case": b.get("case_id"),
                    "file": b.get("original_filename"),
                    "officer": b.get("officer_name")
                })

        if geo_data:
            import pandas as pd
            df_geo = pd.DataFrame(geo_data)

            # High-Resolution Native Streamlit Map (No External Token Required)
            st.map(
                df_geo,
                latitude="lat",
                longitude="lon",
                color="#1D4ED8",
                size=35,
                zoom=6
            )

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown("##### Seized Artifacts Crime Scene GPS Telemetry:")

            # Interactive GPS Exhibit Cards
            cols = st.columns(min(len(geo_data), 3))
            for idx, g in enumerate(geo_data):
                col_target = cols[idx % len(cols)]
                with col_target:
                    gmaps_url = f"https://www.google.com/maps?q={g['lat']},{g['lon']}"
                    st.markdown(f"""
                    <div class="forensic-card" style="padding: 16px; margin-bottom: 12px;">
                        <div style="font-size: 11px; font-weight: 700; color: #1D4ED8; text-transform: uppercase;">
                            Crime Scene #{idx + 1}
                        </div>
                        <div style="font-size: 13.5px; font-weight: 700; color: #0F172A; margin: 4px 0;">
                            {g['file']}
                        </div>
                        <div style="font-size: 12px; color: #64748B;">
                            Case: <strong>{g['case']}</strong><br/>
                            Officer: {g['officer']}<br/>
                            GPS: <code>{g['lat']}, {g['lon']}</code>
                        </div>
                        <div style="margin-top: 10px;">
                            <a href="{gmaps_url}" target="_blank" style="text-decoration: none; font-size: 11.5px; font-weight: 600; color: #2563EB; background: #EFF6FF; padding: 4px 10px; border-radius: 4px; border: 1px solid #BFDBFE; display: inline-block;">
                                View in Google Maps ↗
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Telemetry Table
            with st.expander("Telemetry Coordinates Data Table", expanded=False):
                st.dataframe(df_geo, use_container_width=True)
        else:
            st.info("No GPS coordinates recorded in current ledger.")
