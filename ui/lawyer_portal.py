import streamlit as st
import os
from crypto_chain import (
    get_ledger,
    verify_chain_integrity,
    reverse_search_evidence,
    calculate_file_hash,
    VAULT_DIR
)
from pdf_generator import generate_forensic_pdf, generate_forensic_pdf_bytes, check_block_tampered
from backend.audit_service import lodge_dispute, get_disputes, log_event

def render_lawyer_portal(user: dict):
    # Enterprise Command Header
    st.markdown(f"""
    <div class="enterprise-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="inst-badge lawyer">Legal Counsel & Bar Council</span>
                    <span class="telemetry-beacon">
                        <span class="dot"></span> DISCOVERY VAULT // CONTINUOUS INTEGRITY
                    </span>
                </div>
                <h1>Evidentiary Discovery & Examination Terminal</h1>
                <p>Advocate: <strong>{user.get('full_name')}</strong> | Bar Roll No: <code>{user.get('identifier')}</code> | Division: {user.get('department')}</p>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">
                JURISDICTION: SESSIONS BAR<br/>
                STATUTE: BSA 2023 §63 / IEA §65B
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chain = get_ledger()
    disputes = get_disputes()
    my_disputes = [d for d in disputes if d.get("filed_by") == user.get("full_name")]

    # Operational Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Total Case Exhibits</div>
            <div class="metric-value">{len(chain)}</div>
            <div class="metric-sub">Ledger Available</div>
            """, unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            cases_count = len(set(b.get("case_id") for b in chain)) if chain else 0
            st.markdown(f"""
            <div class="metric-label">Court Dockets Tracked</div>
            <div class="metric-value">{cases_count}</div>
            <div class="metric-sub">Active Docket Records</div>
            """, unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Chain Continuity</div>
            <div class="metric-value" style="color: #059669;">100% Cryptographic</div>
            <div class="metric-sub">Merkle Root Verified</div>
            """, unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Objections Lodged</div>
            <div class="metric-value">{len(my_disputes)}</div>
            <div class="metric-sub">Judicial Bench Review</div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Tabs
    law_tab1, law_tab2, law_tab3, law_tab4 = st.tabs([
        "Exhibit Discovery",
        "Reverse Hash Engine",
        "Section 65B Certificates",
        "Evidentiary Objections"
    ])

    # ---------------- TAB 1: CASE EXHIBITS ----------------
    with law_tab1:
        st.markdown("""
        <div class="forensic-card">
            <h3>1. Electronic Evidence Discovery & Chain Inspection</h3>
            <p>
                Examine electronic exhibits ingested by prosecution authorities. Verify mathematical non-repudiation and custodial timeline continuity.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.info("No electronic exhibits registered in custody ledger.")
        else:
            all_cases = sorted(list(set(b["case_id"] for b in chain)))
            sel_case = st.selectbox("Filter Exhibits by Case Docket Reference:", ["ALL CASES"] + all_cases)

            filtered = chain if sel_case == "ALL CASES" else [b for b in chain if b["case_id"] == sel_case]

            # Check for tamper alert
            any_tampered = any(check_block_tampered(b)[0] for b in chain)
            if any_tampered:
                st.error("🚨 **DEFENSE DISCOVERY ALERT: Bitstream Tampering Detected on Prosecution Exhibits!** The on-disk artifact does not match the immutable genesis hash. Strong statutory grounds exist to file an Objection under BSA 2023 §63 / IEA §65B in Tab 4.")

            for b in filtered:
                is_tampered, current_hash = check_block_tampered(b)
                status_label = "🚨 [TAMPER DETECTED]" if is_tampered else "[PRISTINE BITSTREAM]"
                expander_title = f"{status_label} Exhibit #{b['block_id']}: {b.get('original_filename')} — Case: {b.get('case_id')}"
                
                with st.expander(expander_title, expanded=is_tampered):
                    c1, c2 = st.columns([1.5, 1.5])
                    with c1:
                        st.markdown(f"**Case Docket Reference:** `{b.get('case_id')}` ({b.get('case_type', 'Cyber Crime')})")
                        st.markdown(f"**Prosecution Officer:** {b.get('officer_name')} (`{b.get('badge_id')}`)")
                        st.markdown(f"**Seizure Location:** {b.get('seizure_location')}")
                        st.markdown(f"**Timestamp (UTC):** `{b.get('timestamp')}`")
                        st.markdown(f"**Complainant / Victim:** {b.get('victim_name')}")
                        if b.get("latitude") and b.get("longitude"):
                            st.markdown(f"**Crime Scene Coordinates:** `{b.get('latitude')}, {b.get('longitude')}`")
                    with c2:
                        st.markdown(f"**Original Genesis SHA-256 Digest:**")
                        st.code(b.get("evidence_hash"), language=None)
                        st.markdown(f"**Live Recomputed Hash (Disk Audit):**")
                        st.code(current_hash, language=None)
                        if is_tampered:
                            st.error("Bitstream Discrepancy: File modified post-seizure. Inadmissible under BSA 2023 §63.")
                        else:
                            st.success("Bitstream Authenticity: Strict match with genesis seizure fingerprint.")

                    # Custody Trail Inspection
                    st.markdown("##### Chain of Custody Audit Trail:")
                    trail = b.get("custody_trail", [])
                    if trail:
                        for step in trail:
                            st.markdown(f"- **Step #{step.get('step_no')}** (`{step.get('timestamp')}`): `{step.get('from_entity')}` ➔ `{step.get('to_entity')}` | Purpose: *{step.get('purpose')}* | Challan: `{step.get('challan_id')}`")
                    else:
                        st.caption("No inter-agency transfers recorded for this artifact.")

    # ---------------- TAB 2: REVERSE HASH SEARCH ----------------
    with law_tab2:
        st.markdown("""
        <div class="forensic-card">
            <h3>2. Reverse Hash Search Engine (Artifact Verification)</h3>
            <p>
                Query the Merkle ledger by SHA-256 hash or raw file upload to verify if an exhibit matches an authentic police seizure.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_search_hash, col_search_file = st.columns(2)

        with col_search_hash:
            query_hash = st.text_input("Enter 64-character SHA-256 Digest:", placeholder="e.g. f793c5fd34c08961faceea...")
            if st.button("Query Ledger Fingerprint", use_container_width=True):
                if not query_hash:
                    st.warning("Please provide a valid SHA-256 hash digest.")
                else:
                    found, match, err = reverse_search_evidence(query_hash.strip())
                    if found:
                        st.success(f"""
                        **Cryptographic Match Confirmed:**
                        - **Block Index:** Block #{match['block_id']}
                        - **Case Docket:** {match.get('case_id')} ({match.get('case_type')})
                        - **Artifact Name:** `{match.get('original_filename')}`
                        - **Seizing Officer:** {match.get('officer_name')} (`{match.get('badge_id')}`)
                        - **Timestamp:** {match.get('timestamp')}
                        """)
                    else:
                        st.error(f"{err}")

        with col_search_file:
            verify_file = st.file_uploader("Upload Suspicious Artifact to Verify Integrity:", type=None, key="law_ver_f")
            if verify_file is not None:
                computed_hash = calculate_file_hash(verify_file.getvalue())
                st.markdown(f"**Computed SHA-256:** `{computed_hash}`")
                found, match, err = reverse_search_evidence(computed_hash)
                if found:
                    st.success(f"Authenticity Verified: Matches Exhibit #{match['block_id']} in Case {match.get('case_id')}")
                else:
                    st.error("Bitstream Mismatch: File does not exist in prosecution ledger or was altered post-seizure.")

    # ---------------- TAB 3: SECTION 65B CERTIFICATES ----------------
    with law_tab3:
        st.markdown("""
        <div class="forensic-card">
            <h3>3. Section 65B Statutory Legal Compliance Certificates</h3>
            <p>
                Generate and download court-admissible Section 65B certificates formatted under the Indian Evidence Act / Section 63 BSA 2023 with scannable verification seals.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.warning("No electronic evidence recorded in ledger.")
        else:
            with st.container(border=True):
                block_opts = {f"Exhibit #{b['block_id']}: {b.get('original_filename')} ({b.get('case_id')})": b['block_id'] for b in chain}
                target_block_sel = st.selectbox("Select Exhibit for Section 65B Certificate:", list(block_opts.keys()), key="lawyer_cert_sel")
                target_b_id = block_opts[target_block_sel]
                target_block = next(b for b in chain if b["block_id"] == target_b_id)

                # Exhibit & Officer Preview
                st.markdown(f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 16px; margin: 8px 0 14px 0;">
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; font-size: 12.5px;">
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block;">FIR Docket</span>
                            <strong style="color: #2563EB; font-family: 'JetBrains Mono', monospace;">{target_block.get('case_id')}</strong>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block;">Seizing Officer</span>
                            <strong style="color: #0F172A;">{target_block.get('officer_name')}</strong> <code>{target_block.get('badge_id')}</code>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 11px; text-transform: uppercase; font-weight: 600; display: block;">Seizure Timestamp</span>
                            <span style="color: #0F172A;">{target_block.get('timestamp')}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                is_target_tampered, curr_hash = check_block_tampered(target_block)
                if is_target_tampered:
                    st.error(f"""
                    🚨 **CRITICAL ADMISSIBILITY BREACH: BITSTREAM MUTATION DETECTED ON EXHIBIT #{target_b_id}!**  
                    - **Genesis Seizure SHA-256:** `{target_block.get('evidence_hash')}`  
                    - **Current Physical Disk SHA-256:** `{curr_hash}`  
                    - **Admissibility Determination:** **INADMISSIBLE UNDER BSA 2023 §63 / IEA §65B**  
                    - *The Certificate generated below will be rendered as an official FORENSIC BREACH & TAMPER REPORT.*
                    """)

                col_pdf_l, col_pdf_r = st.columns([2, 1])
                with col_pdf_l:
                    magistrate_name = st.text_input("Designated Court / Bench", value="Hon. Principal Sessions Judge, Cyber Court", key=f"mag_{target_b_id}")
                    court_location = st.text_input("Judicial District", value="City Civil & Sessions Court, Chennai", key=f"loc_{target_b_id}")
                    cert_pdf_bytes = generate_forensic_pdf_bytes(target_block, magistrate_name=magistrate_name, court_location=court_location)

                    btn_lbl = f"🚨 Download Section 65B Inadmissibility Certificate (PDF) - Exhibit #{target_b_id}" if is_target_tampered else f"Download Signed Section 65B Certificate (PDF) - Exhibit #{target_b_id}"
                    st.download_button(
                        label=btn_lbl,
                        data=cert_pdf_bytes,
                        file_name=f"Section65B_Certificate_Case_{target_block.get('case_id')}_Block_{target_b_id}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                        key=f"btn_cert_{target_b_id}"
                    )
                with col_pdf_r:
                    st.markdown("""
                    <div style="background: #EEF2FF; padding: 14px; border-radius: 8px; border: 1px solid #C7D2FE; font-size: 12px; color: #312E81; line-height: 1.5;">
                        <strong>Supreme Court Precedent:</strong> Under <em>Arjun Panditrao Khotkar (2020)</em>, secondary electronic records require contemporaneous Section 65B certification for courtroom admissibility.
                    </div>
                    """, unsafe_allow_html=True)

    # ---------------- TAB 4: LODGE DISPUTE ----------------
    with law_tab4:
        st.markdown("""
        <div class="forensic-card">
            <h3>4. Formal Evidentiary Dispute & Objection Filing</h3>
            <p>
                File formal legal objections regarding chain of custody discontinuity, timestamp discrepancies, or missing write-blocker attestations for determination by the Presiding Bench.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.info("No evidence records available to dispute.")
        else:
            with st.form("dispute_form"):
                block_to_dispute = st.selectbox(
                    "Select Contested Exhibit:",
                    [f"Block #{b['block_id']}: {b.get('original_filename')} ({b.get('case_id')})" for b in chain]
                )
                dispute_block_id = int(block_to_dispute.split("#")[1].split(":")[0])
                dispute_case_id = block_to_dispute.split("(")[1].split(")")[0]

                legal_ground = st.selectbox(
                    "Statutory Ground of Objection:",
                    [
                        "Section 65B(2) Condition Breach: Computer not in lawful operational custody",
                        "Chain of Custody Discontinuity: Unaccounted time lapse during police transit",
                        "Allegation of Post-Seizure Modification: Bitstream mismatch between seizure and lab",
                        "Absence of Hardware Write-Blocker Attestation at Crime Scene",
                        "Disputed Trojan Masquerade: Hostile payload injected into client device"
                    ]
                )
                dispute_details = st.text_area("Evidentiary Arguments & Legal Grounds", placeholder="Detail specific grounds for exclusion by the Presiding Judge...")

                submit_dispute = st.form_submit_button("Submit Formal Objection to Bench", use_container_width=True, type="primary")

                if submit_dispute:
                    if not dispute_details.strip():
                        st.warning("Please specify detailed legal grounds for objection.")
                    else:
                        ok, msg = lodge_dispute(user, dispute_case_id, dispute_block_id, dispute_details, legal_ground)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

        # Show existing filed disputes
        if my_disputes:
            st.markdown("##### Filed Objections Docket:")
            for d in reversed(my_disputes):
                with st.expander(f"Dispute {d.get('dispute_id')} — Case: {d.get('case_id')} | Status: {d.get('status')}", expanded=True):
                    st.markdown(f"**Filed Date:** {d.get('timestamp')}")
                    st.markdown(f"**Legal Ground:** {d.get('legal_ground')}")
                    st.markdown(f"**Arguments:** {d.get('reason')}")
                    if d.get("ruling"):
                        st.markdown(f"**Judicial Decree by {d.get('ruled_by')}:**")
                        st.info(d.get("ruling"))
