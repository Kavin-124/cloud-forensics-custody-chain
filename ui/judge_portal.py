import streamlit as st
import os
from crypto_chain import (
    get_ledger,
    verify_chain_integrity,
    VAULT_DIR,
    CLOUD_VAULT_DIR
)
from backend.audit_service import get_disputes, record_judicial_ruling, log_event
from pdf_generator import generate_forensic_pdf

def render_judge_portal(user: dict):
    # Enterprise Command Header
    st.markdown(f"""
    <div class="enterprise-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="inst-badge judge">Judicial Bench & Court of Record</span>
                    <span class="telemetry-beacon">
                        <span class="dot"></span> BENCH ACTIVE // ADMISSIBILITY DETERMINATION
                    </span>
                </div>
                <h1>Presiding Magistrate Judicial Command Terminal</h1>
                <p>Presiding Officer: <strong>{user.get('full_name')}</strong> | Bench ID: <code>{user.get('identifier')}</code> | Jurisdiction: {user.get('department')}</p>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">
                COURT OF RECORD: SESSIONS<br/>
                STATUTORY SEAL: BSA 2023 §63
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chain = get_ledger()
    disputes = get_disputes()
    pending_disputes = [d for d in disputes if d.get("status") == "PENDING_JUDICIAL_REVIEW"]

    # Operational Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cases in Trial Review</div>
            <div class="metric-value">{len(set(b['case_id'] for b in chain)) if chain else 0}</div>
            <div class="metric-sub">Active Judicial Dockets</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Pending Evidentiary Objections</div>
            <div class="metric-value" style="color: {'#DC2626' if pending_disputes else '#059669'};">{len(pending_disputes)}</div>
            <div class="metric-sub">Awaiting Judicial Determination</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        integrity_res = verify_chain_integrity()
        all_ok = integrity_res[0]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Merkle Ledger Integrity</div>
            <div class="metric-value" style="color: {'#059669' if all_ok else '#DC2626'};">{'VALIDATED (Unbroken)' if all_ok else 'ANOMALY DETECTED'}</div>
            <div class="metric-sub">NIST SHA-256 Chaining</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Admissibility Mandate</div>
            <div class="metric-value">Section 65B(4)</div>
            <div class="metric-sub">Indian Evidence Act / BSA 2023</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Tabs
    jdg_tab1, jdg_tab2, jdg_tab3 = st.tabs([
        "Evidentiary Determinations",
        "Cryptographic Audit Terminal",
        "Mobile QR Verification Endpoint"
    ])

    # ---------------- TAB 1: JUDICIAL RULINGS ----------------
    with jdg_tab1:
        st.markdown("""
        <div class="forensic-card">
            <h3>1. Admissibility Determinations on Defense Objections</h3>
            <p>
                Under Section 65B of the Indian Evidence Act and Section 63 of BSA 2023, the Court determines the legal admissibility
                and cryptographic continuity of electronic records prior to trial marking.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not disputes:
            st.info("No objections currently filed for judicial determination.")
        else:
            for d in reversed(disputes):
                status = d.get("status")
                is_pending = (status == "PENDING_JUDICIAL_REVIEW")

                status_label = f"[{status}]"
                with st.expander(f"{status_label} Dispute {d.get('dispute_id')} — Case: {d.get('case_id')} (Exhibit #{d.get('block_id')})", expanded=is_pending):
                    col_l, col_r = st.columns([1.5, 1])
                    with col_l:
                        st.markdown(f"**Dispute Reference:** `{d.get('dispute_id')}`")
                        st.markdown(f"**Counsel on Record:** {d.get('filed_by')} (`{d.get('bar_id')}`)")
                        st.markdown(f"**Filing Timestamp (UTC):** `{d.get('timestamp')}`")
                        st.markdown(f"**Statutory Ground:** {d.get('legal_ground')}")
                        st.markdown(f"**Counsel's Affidavit:**")
                        st.write(d.get("reason"))

                    with col_r:
                        target_b = next((b for b in chain if b["block_id"] == d["block_id"]), None)
                        if target_b:
                            st.markdown(f"**Artifact Name:** `{target_b.get('original_filename')}`")
                            st.markdown(f"**SHA-256 Digest:**")
                            st.code(target_b.get("evidence_hash")[:32] + "...", language=None)
                            st.markdown(f"**Seizing Officer:** {target_b.get('officer_name')}")

                    if is_pending:
                        st.markdown("---")
                        st.markdown("##### Pronounce Judicial Admissibility Decree:")
                        col_r1, col_r2 = st.columns([1.2, 2])
                        with col_r1:
                            ruling_choice = st.selectbox(
                                "Judicial Determination:",
                                [
                                    "OBJECTION_OVERRULED (Evidence Admitted under Sec 65B)",
                                    "OBJECTION_SUSTAINED (Evidence Excluded / Tamper Found)",
                                    "REFERRED_FOR_INDEPENDENT_FSL_AUDIT"
                                ],
                                key=f"r_choice_{d['dispute_id']}"
                            )
                        with col_r2:
                            judicial_order_text = st.text_area(
                                "Official Reasoning & Judicial Decree:",
                                value="Having examined the NIST SHA-256 hash chaining and finding no mathematical discontinuity in custody, the objection is overruled and the evidence is admitted under Section 65B(4).",
                                key=f"r_text_{d['dispute_id']}"
                            )

                        if st.button(f"Sign & Seal Judicial Decree ({d['dispute_id']})", type="primary", key=f"btn_r_{d['dispute_id']}"):
                            clean_ruling = ruling_choice.split(" ")[0]
                            ok, msg = record_judicial_ruling(user, d["dispute_id"], clean_ruling, judicial_order_text)
                            if ok:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        st.markdown("---")
                        st.markdown(f"**Judicial Verdict:** `{status}` by **{d.get('ruled_by')}** on `{d.get('ruling_timestamp')}`")
                        st.info(d.get("ruling"))

    # ---------------- TAB 2: JUDICIAL INTEGRITY AUDIT ----------------
    with jdg_tab2:
        st.markdown("""
        <div class="forensic-card">
            <h3>2. Courtroom Cryptographic Merkle Tree Audit</h3>
            <p>
                Traverse SHA-256 parent-child linkages and compute bitstream digests across all on-disk artifacts in the custodial repository.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Execute Cryptographic Ledger Audit", type="primary", use_container_width=True):
            with st.spinner("Traversing Merkle hash chain and recomputing disk bitstream hashes..."):
                integrity_res = verify_chain_integrity()
                all_ok = integrity_res[0]
                results = integrity_res[-1]
                total_blocks = len(results)
                if all_ok:
                    st.success(f"Audit Complete: All {total_blocks} exhibits are mathematically verified, pristine, and uncompromised.")
                else:
                    st.error("Integrity Anomaly Detected: One or more on-disk artifacts have been modified post-seizure.")

                for r in results:
                    st.write(f"- Block #{r['block_id']}: {r['filename']} — **{r['status']}** (SHA-256 verification)")

    # ---------------- TAB 3: QR VERIFICATION & PUBLIC PORTAL ----------------
    with jdg_tab3:
        st.markdown("""
        <div class="forensic-card">
            <h3>3. Smartphone QR Verification & Open Public Gateway</h3>
            <p>
                In open court proceedings, magistrates, advocates, and expert witnesses can scan the cryptographic QR seal embedded on any Section 65B PDF certificate using any standard smartphone camera.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 20px; text-align: center;">
            <div style="font-size: 13px; font-weight: 600; color: #0F172A; margin-bottom: 8px;">
                Public Courtroom Verification Endpoint:
            </div>
            <div style="font-size: 13.5px; font-family: 'JetBrains Mono', monospace; background: #F8FAFC; color: #0F172A; padding: 8px 16px; border-radius: 6px; display: inline-block; border: 1px solid #CBD5E1;">
                https://fair-holiday-ixjm8.ship.place/
            </div>
            <p style="font-size: 12px; color: #64748B; margin-top: 10px;">
                Direct cryptographic proof retrieval without requiring client software installation on bench devices.
            </p>
        </div>
        """, unsafe_allow_html=True)
