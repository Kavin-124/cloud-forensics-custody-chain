import streamlit as st
from backend.auth_service import authenticate_user, get_user_by_identifier

def render_login_page():
    # Enterprise Institutional Header
    st.markdown("""
    <div style="text-align: center; max-width: 680px; margin: 35px auto 25px auto;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px; background: #0B0F19; border: 1px solid #1E293B; border-radius: 12px; box-shadow: 0 4px 14px rgba(11,15,25,0.15); margin-bottom: 14px;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <circle cx="12" cy="11" r="3"/>
                <path d="M12 14v3"/>
            </svg>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; color: #2563EB; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 4px;">
            National Digital Forensic Evidence Vault
        </div>
        <h1 style="font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 700; color: #0F172A; margin: 0; letter-spacing: -0.02em;">
            Cryptographic Chain of Custody System
        </h1>
        <p style="font-size: 13.5px; color: #475569; margin: 6px 0 14px 0; font-weight: 400;">
            High Court of Judicature & State Cyber Crime Directorate • Sovereign Cloud Node-01
        </p>
        <div style="display: flex; justify-content: center; margin-bottom: 6px;">
            <span class="telemetry-beacon">
                <span class="dot"></span>
                IMMUTABLE CLOUD LEDGER: ONLINE // COMPLIANT WITH BSA 2023 §63 & IEA §65B
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.05); margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 12px;">
                <div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 700; color: #0F172A; letter-spacing: -0.01em;">
                        Authentication Gateway
                    </div>
                    <div style="font-size: 12px; color: #64748B;">
                        Select designated institutional portal:
                    </div>
                </div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10.5px; font-weight: 600; background: #F1F5F9; color: #475569; padding: 3px 8px; border-radius: 4px; border: 1px solid #E2E8F0;">
                    HMAC-SHA256
                </span>
            </div>
        """, unsafe_allow_html=True)

        portal_tab1, portal_tab2, portal_tab3 = st.tabs([
            "Law Enforcement",
            "Judicial Chamber & Bar",
            "System Registrar"
        ])

        # ---------------- POLICE PORTAL LOGIN ----------------
        with portal_tab1:
            st.markdown("""
            <div style="padding: 4px 0 10px 0;">
                <span class="inst-badge police">Law Enforcement Division</span>
                <p style="font-size: 12.5px; color: #64748B; margin: 6px 0 2px 0;">
                    Authorized for electronic evidence seizure, GPS satellite logging, magic-byte inspection, and custody handovers.
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("police_login_form"):
                badge_id = st.text_input("Officer Badge ID / Service Token", placeholder="e.g. CB-TN-4091", key="pol_id")
                password = st.text_input("Security Passphrase", type="password", placeholder="Enter security passphrase", key="pol_pwd")
                submit_police = st.form_submit_button("Authenticate Session →", use_container_width=True, type="primary")

                if submit_police:
                    success, user, msg = authenticate_user(badge_id, password, expected_role="police")
                    if success:
                        st.session_state["user"] = user
                        st.session_state["authenticated"] = True
                        st.success(f"Session established: {user['full_name']} ({user['department']})")
                        st.rerun()
                    else:
                        st.error(msg)

        # ---------------- COURT PORTAL LOGIN ----------------
        with portal_tab2:
            st.markdown("""
            <div style="padding: 4px 0 10px 0;">
                <span class="inst-badge lawyer">Judicial Proceedings</span>
                <p style="font-size: 12.5px; color: #64748B; margin: 6px 0 2px 0;">
                    Designated jurisdiction under the High Court & Sessions Bar:
                </p>
            </div>
            """, unsafe_allow_html=True)

            court_subrole = st.radio(
                "Designation Wing:",
                ["Legal Counsel / Advocate", "Presiding Magistrate / Sessions Bench"],
                horizontal=True
            )

            if "Legal Counsel" in court_subrole:
                with st.form("lawyer_login_form"):
                    st.caption("Advocate / Legal Discovery Registry")
                    law_user = st.text_input("Bar Council Roll / Username", placeholder="e.g. advocate_kavin", key="law_u")
                    law_pwd = st.text_input("Account Passphrase", type="password", placeholder="Enter passphrase", key="law_p")
                    submit_lawyer = st.form_submit_button("Authenticate Session →", use_container_width=True, type="primary")

                    if submit_lawyer:
                        success, user, msg = authenticate_user(law_user, law_pwd, expected_role="lawyer")
                        if success:
                            st.session_state["user"] = user
                            st.session_state["authenticated"] = True
                            st.success(f"Session established: {user['full_name']}")
                            st.rerun()
                        else:
                            st.error(msg)
            else:
                with st.form("judge_login_form"):
                    st.caption("Magistrate Bench / Court of Record Authority")
                    judge_user = st.text_input("Judicial Officer Identifier", placeholder="e.g. justice_sharma", key="jdg_u")
                    judge_pwd = st.text_input("Bench Security Token", type="password", placeholder="Enter bench token", key="jdg_p")
                    submit_judge = st.form_submit_button("Authenticate Session →", use_container_width=True, type="primary")

                    if submit_judge:
                        success, user, msg = authenticate_user(judge_user, judge_pwd, expected_role="judge")
                        if success:
                            st.session_state["user"] = user
                            st.session_state["authenticated"] = True
                            st.success(f"Session established: {user['full_name']}")
                            st.rerun()
                        else:
                            st.error(msg)

        # ---------------- ADMIN PORTAL LOGIN ----------------
        with portal_tab3:
            st.markdown("""
            <div style="padding: 4px 0 10px 0;">
                <span class="inst-badge admin">Root Key Authority</span>
                <p style="font-size: 12.5px; color: #64748B; margin: 6px 0 2px 0;">
                    Restricted master access. Only the System Registrar can provision personnel and manage nodes.
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("admin_login_form"):
                admin_user = st.text_input("Administrator Username", placeholder="e.g. admin", key="adm_u")
                admin_pwd = st.text_input("Master Passphrase", type="password", placeholder="Enter master passphrase", key="adm_p")
                submit_admin = st.form_submit_button("Authenticate Session →", use_container_width=True, type="primary")

                if submit_admin:
                    success, user, msg = authenticate_user(admin_user, admin_pwd, expected_role="admin")
                    if success:
                        st.session_state["user"] = user
                        st.session_state["authenticated"] = True
                        st.success(f"Session established: {user['full_name']}")
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

        # Institutional Examiner / Developer Sandbox
        st.markdown("""
        <div style="margin-top: 14px; text-align: center;">
            <div style="font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 8px;">
                Institutional Sandbox (Evaluation Mode)
            </div>
        </div>
        """, unsafe_allow_html=True)

        demo_c1, demo_c2, demo_c3, demo_c4 = st.columns(4)
        with demo_c1:
            if st.button("Cyber Cell", use_container_width=True):
                st.session_state["user"] = get_user_by_identifier("CB-TN-4091")
                st.session_state["authenticated"] = True
                st.rerun()
        with demo_c2:
            if st.button("High Court Bar", use_container_width=True):
                st.session_state["user"] = get_user_by_identifier("advocate_kavin")
                st.session_state["authenticated"] = True
                st.rerun()
        with demo_c3:
            if st.button("Sessions Bench", use_container_width=True):
                st.session_state["user"] = get_user_by_identifier("justice_sharma")
                st.session_state["authenticated"] = True
                st.rerun()
        with demo_c4:
            if st.button("Chief Registrar", use_container_width=True):
                st.session_state["user"] = get_user_by_identifier("admin")
                st.session_state["authenticated"] = True
                st.rerun()

        # Statutory Warning & Credentials Reference
        st.markdown("""
        <div style="margin-top: 16px; margin-bottom: 12px; padding: 12px 14px; background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; font-size: 12.5px; color: #475569; line-height: 1.5;">
            <strong>Statutory Access Control:</strong> Under Section 63 of the Bharatiya Sakshya Adhiniyam 2023 and Section 65B of the Indian Evidence Act, 
            public self-registration is strictly prohibited. All cryptographic identities must be sanctioned by the <strong>Forensic System Administrator</strong>.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Personnel Directory & Access Credentials", expanded=False):
            st.markdown("""
            | Division | Identifier | Passphrase | Assigned Personnel |
            | :--- | :--- | :--- | :--- |
            | **Law Enforcement** | `CB-TN-4091` | `police123` | Insp. R. Vikram (Cyber Crime Wing) |
            | **Counsel & Bar** | `advocate_kavin` | `lawyer123` | Adv. Kavin R. (High Court Bar) |
            | **Judicial Bench** | `justice_sharma` | `judge123` | Hon. Justice S. Sharma (Sessions Bench) |
            | **Root Authority** | `admin` | `admin123` | Chief Forensic Registrar (Cloud Node) |
            """)
