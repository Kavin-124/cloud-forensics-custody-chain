import streamlit as st
import os
from backend.auth_service import get_all_users, register_new_user, delete_user
from backend.audit_service import get_audit_logs, log_event
from crypto_chain import (
    get_ledger,
    simulate_tampering,
    auto_heal_all_tampered,
    auto_heal_evidence,
    get_storage_stats,
    reset_all_evidence,
    verify_chain_integrity,
    VAULT_DIR,
    CLOUD_VAULT_DIR
)
from pdf_generator import check_block_tampered

def render_admin_portal(user: dict):
    # Enterprise Command Header
    st.markdown(f"""
    <div class="enterprise-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="inst-badge admin">Root Key Authority</span>
                    <span class="telemetry-beacon">
                        <span class="dot"></span> MASTER GOVERNANCE // ACCESS LEVEL: ROOT
                    </span>
                </div>
                <h1>Forensic Identity & Ledger Governance Center</h1>
                <p>Master Administrator: <strong>{user.get('full_name')}</strong> | Node ID: <code>{user.get('identifier')}</code> | Division: {user.get('department')}</p>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94A3B8;">
                NODE: ROOT-01-TAMILNADU<br/>
                CONSENSUS: HMAC-SHA256
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    users = get_all_users()
    logs = get_audit_logs()
    chain = get_ledger()
    storage_stats = get_storage_stats()

    # Operational Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Provisioned Personnel</div>
            <div class="metric-value">{len(users)}</div>
            <div class="metric-sub">Police, Counsel, Bench Accounts</div>
            """, unsafe_allow_html=True)
    with m2:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Audit Telemetry Events</div>
            <div class="metric-value">{len(logs)}</div>
            <div class="metric-sub">Immutable Trace Log Entries</div>
            """, unsafe_allow_html=True)
    with m3:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Active Ledger Blocks</div>
            <div class="metric-value">{len(chain)}</div>
            <div class="metric-sub">Cryptographically Bound Merkle Nodes</div>
            """, unsafe_allow_html=True)
    with m4:
        with st.container(border=True):
            st.markdown(f"""
            <div class="metric-label">Vault Storage Volume</div>
            <div class="metric-value">{storage_stats.get('total_size_mb', 0):.2f} MB</div>
            <div class="metric-sub">Local + Cloud Synchronized</div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Tabs
    adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs([
        "Identity Provisioning",
        "Audit Telemetry",
        "Tamper & Auto-Healing",
        "Vault Storage & Purge"
    ])

    # ---------------- TAB 1: USER PROVISIONING ----------------
    with adm_tab1:
        st.markdown("""
        <div class="forensic-card">
            <h3>1. Institutional Identity & Access Provisioning</h3>
            <p>
                In compliance with statutory non-repudiation mandates, all judicial, legal, and law enforcement accounts must be formally provisioned by the Root Key Authority.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_reg, col_list = st.columns([1.4, 1.6])

        with col_reg:
            st.markdown("##### Provision New Institutional Account")
            with st.form("admin_create_user_form"):
                new_role = st.selectbox(
                    "Division Role:",
                    ["police", "lawyer", "judge", "admin"],
                    format_func=lambda x: "Law Enforcement Officer" if x == "police" else ("Legal Counsel / Advocate" if x == "lawyer" else ("Presiding Magistrate / Judge" if x == "judge" else "System Administrator"))
                )

                new_name = st.text_input("Full Personnel Name", placeholder="e.g. Insp. K. Murugan")
                new_uname = st.text_input("Username / Service Badge (Login ID)", placeholder="e.g. CB-TN-8099 or advocate_ravi")
                new_ident = st.text_input("Official Registration / Bench Token", placeholder="e.g. CB-TN-8099 or BAR-TN-4011/2023")
                new_dept = st.text_input("Institutional Wing / Jurisdiction", placeholder="e.g. Special Cyber Crime Branch, Karur")
                new_pwd = st.text_input("Initial Access Passphrase", type="password", placeholder="Assign secure passphrase")

                submit_user = st.form_submit_button("Provision Credentials", type="primary", use_container_width=True)

                if submit_user:
                    ok, msg = register_new_user(user, new_name, new_uname, new_role, new_ident, new_dept, new_pwd)
                    if ok:
                        log_event(user.get("full_name"), "ADMIN", "USER_REGISTER", f"Created {new_role.upper()} account '{new_name}' ({new_uname})")
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        with col_list:
            st.markdown("##### Registered Personnel Directory:")
            user_table_data = []
            for u in users:
                user_table_data.append({
                    "Role": u.get("role").upper(),
                    "Personnel Name": u.get("full_name"),
                    "Identifier": u.get("identifier"),
                    "Division": u.get("department")
                })
            import pandas as pd
            st.dataframe(pd.DataFrame(user_table_data), use_container_width=True)

    # ---------------- TAB 2: AUDIT LOG ----------------
    with adm_tab2:
        st.markdown("""
        <div class="forensic-card">
            <h3>2. Immutable System Audit Telemetry Log</h3>
            <p>
                Every authentication event, electronic artifact intake, custody transfer, judicial decree, and tamper detection trigger is permanently recorded in chronological sequence.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not logs:
            st.info("No audit telemetry recorded in current ledger.")
        else:
            import pandas as pd
            df_logs = pd.DataFrame(reversed(logs))
            st.dataframe(df_logs[["timestamp", "actor", "role", "action", "details", "status"]], use_container_width=True)

    # ---------------- TAB 3: TAMPER SIMULATION & AUTO-HEAL ----------------
    with adm_tab3:
        st.markdown("""
        <div class="forensic-card">
            <h3>3. Bitstream Tamper Injection & Autonomous Cloud Self-Healing</h3>
            <p>
                Demonstrate the forensic architecture's resilience under malicious insider attack scenarios. Deliberately mutate bytes on local disk, 
                observe instantaneous detection, and verify sub-millisecond restoration from the pristine cloud replica.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if not chain:
            st.warning("No evidence in ledger to simulate tampering.")
        else:
            # Check for any tampered blocks across ledger
            tampered_blocks = [b for b in chain if check_block_tampered(b)[0]]
            if tampered_blocks:
                st.error(f"""
                🚨 **CRITICAL FORENSIC INTEGRITY ALERT: {len(tampered_blocks)} Artifact(s) Compromised on Local Disk!**  
                Unauthorized bitstream mutation detected! Disk hashes deviate from immutable genesis fingerprints.
                Click **"Execute Cloud Autonomous Self-Healing"** or use individual restore buttons below to repair.
                """)

            col_t1, col_t2 = st.columns(2)

            with col_t1:
                with st.container(border=True):
                    st.markdown("##### 🔴 Adversarial Tamper Injection")
                    st.markdown("<p style='font-size: 12px; color: #64748B;'>Select an exhibit to inject malicious payload bytes into its local vault binary.</p>", unsafe_allow_html=True)
                    target_block = st.selectbox(
                        "Select Evidence Artifact to Mutate:",
                        [f"Block #{b['block_id']}: {b.get('original_filename')} ({b.get('case_id')})" for b in chain],
                        key="admin_tamper_select"
                    )
                    b_id = int(target_block.split("#")[1].split(":")[0])

                    if st.button("Inject Unauthorized Modification (Corrupt Bitstream)", type="primary", use_container_width=True, key="btn_inject_tamper"):
                        tamper_ok, msg = simulate_tampering(b_id)
                        if tamper_ok:
                            log_event(user.get("full_name"), "ADMIN", "SIMULATE_TAMPER", f"Artificially modified Block #{b_id} for demonstration")
                            st.toast(f"Tampered Block #{b_id} successfully!", icon="🚨")
                            st.error(f"🚨 **Tamper Injected Successfully:** Modified Block #{b_id}. Its local disk hash will now mismatch the genesis hash!")
                            st.rerun()
                        else:
                            st.warning(msg)

            with col_t2:
                with st.container(border=True):
                    st.markdown("##### 🟢 Autonomous Cloud Disaster Recovery")
                    st.markdown("""
                    <p style='font-size: 12px; color: #64748B;'>
                    Queries synchronized pristine replica in <code>cloud_vault/</code> and restores corrupted bitstreams in under 1 millisecond.
                    </p>
                    """, unsafe_allow_html=True)
                    if st.button("Execute Cloud Autonomous Self-Healing", use_container_width=True, key="btn_heal_all"):
                        healed_count, results = auto_heal_all_tampered()
                        log_event(user.get("full_name"), "ADMIN", "AUTO_HEAL", f"Triggered autonomous restore for {healed_count} items")
                        if healed_count > 0:
                            st.toast(f"Restored {healed_count} artifacts!", icon="✅")
                            st.success(f"✓ **Disaster Recovery Complete:** Successfully restored {healed_count} corrupted exhibit(s) from cloud mirror.")
                            st.rerun()
                        else:
                            st.info("✓ All on-disk exhibits are currently pristine and in 100% cryptographic agreement.")

            st.markdown("---")
            st.markdown("##### 🛡️ Live Evidence Vault Integrity Monitor")

            for b in chain:
                is_tampered, disk_hash = check_block_tampered(b)
                with st.container(border=True):
                    col_b1, col_b2, col_b3 = st.columns([2, 2.5, 1.2])
                    with col_b1:
                        st.markdown(f"**Exhibit #{b['block_id']}:** `{b.get('original_filename')}`")
                        st.markdown(f"Case: **{b.get('case_id')}** | Officer: {b.get('officer_name')}")
                    with col_b2:
                        st.markdown(f"Genesis SHA-256: `{b.get('evidence_hash')[:24]}...`")
                        if is_tampered:
                            st.markdown(f"Live Disk SHA-256: <code style='color: #DC2626; font-weight: 700;'>{disk_hash[:24]}... (MISMATCH)</code>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"Live Disk SHA-256: <code style='color: #059669;'>{disk_hash[:24]}... (MATCH)</code>", unsafe_allow_html=True)
                    with col_b3:
                        if is_tampered:
                            st.markdown("<span style='font-size: 11px; font-weight: 700; color: #DC2626; background: #FEF2F2; padding: 4px 8px; border-radius: 4px; border: 1px solid #FECACA; display: inline-block;'>🚨 TAMPERED</span>", unsafe_allow_html=True)
                            if st.button("Auto-Heal ➔", key=f"heal_single_{b['block_id']}", use_container_width=True):
                                ok, h_msg = auto_heal_evidence(b["block_id"])
                                if ok:
                                    st.toast(f"Healed Block #{b['block_id']}!", icon="✅")
                                    st.rerun()
                        else:
                            st.markdown("<span style='font-size: 11px; font-weight: 700; color: #059669; background: #ECFDF5; padding: 4px 8px; border-radius: 4px; border: 1px solid #A7F3D0; display: inline-block;'>✓ PRISTINE</span>", unsafe_allow_html=True)

    # ---------------- TAB 4: RESET DATA ----------------
    with adm_tab4:
        st.markdown("""
        <div class="forensic-card">
            <h3>4. Storage Subsystem & Repository Reset</h3>
            <p>
                Purge demonstration evidence artifacts and reinitialize the Merkle ledger for fresh trial examinations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Reinitialize Demonstration Ledger (Purge Vaults)", use_container_width=True):
            reset_all_evidence()
            log_event(user.get("full_name"), "ADMIN", "SYSTEM_RESET", "Purged evidence vault and reset ledger")
            st.success("Demonstration ledger purged. Institutional user accounts remain active.")
            st.rerun()
