import streamlit as st
import os
from ui.theme import apply_pristine_light_theme
from ui.login_page import render_login_page
from ui.police_portal import render_police_portal
from ui.lawyer_portal import render_lawyer_portal
from ui.judge_portal import render_judge_portal
from ui.admin_portal import render_admin_portal
from backend.auth_service import get_user_by_identifier

st.set_page_config(
    page_title="National Forensic Repository | Cryptographic Chain of Custody",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply bespoke Enterprise Sovereign Theme (Inter + JetBrains Mono)
apply_pristine_light_theme()

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# If not logged in, show the Multi-Portal Authentication Gateway
if not st.session_state["authenticated"] or not st.session_state["user"]:
    render_login_page()
else:
    user = st.session_state["user"]
    user_role = user.get("role", "police").lower()

    # Enterprise Top Navigation Bar
    nav_c1, nav_c2, nav_c3 = st.columns([2.5, 1.4, 0.7])
    with nav_c1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 2px 0 10px 0;">
            <div style="width: 38px; height: 38px; background: #0B0F19; border: 1px solid #1E293B; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #38BDF8;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    <circle cx="12" cy="11" r="3"/>
                    <path d="M12 14v3"/>
                </svg>
            </div>
            <div>
                <div style="font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 700; color: #0F172A; letter-spacing: -0.02em;">
                    National Forensic Repository // Merkle Custody Engine
                </div>
                <div style="font-size: 12px; color: #64748B; font-weight: 400;">
                    High Court Judicial Repository & State Cyber Directorate • Node-01
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with nav_c2:
        roles_map = {
            "police": "Law Enforcement (Insp. Vikram)",
            "lawyer": "Legal Counsel (Adv. Kavin)",
            "judge": "Sessions Bench (Hon. Justice Sharma)",
            "admin": "Root Authority (Chief Registrar)"
        }
        user_ids = {
            "Law Enforcement (Insp. Vikram)": "CB-TN-4091",
            "Legal Counsel (Adv. Kavin)": "advocate_kavin",
            "Sessions Bench (Hon. Justice Sharma)": "justice_sharma",
            "Root Authority (Chief Registrar)": "admin"
        }
        current_label = roles_map.get(user_role, "Law Enforcement (Insp. Vikram)")
        role_keys = list(user_ids.keys())
        current_idx = role_keys.index(current_label) if current_label in role_keys else 0

        switched = st.selectbox(
            "Terminal Context",
            role_keys,
            index=current_idx,
            key="viva_role_switch",
            label_visibility="collapsed"
        )
        if user_ids[switched] != user.get("identifier") and user_ids[switched] != user.get("username"):
            st.session_state["user"] = get_user_by_identifier(user_ids[switched])
            st.rerun()

    with nav_c3:
        if st.button("Sign Out", use_container_width=True, type="secondary"):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.rerun()

    st.markdown("<hr style='margin: 4px 0 18px 0; border: none; border-top: 1px solid #E2E8F0;'/>", unsafe_allow_html=True)

    # Route dynamically to specialized Role Interface
    if user_role == "police":
        render_police_portal(user)
    elif user_role == "lawyer":
        render_lawyer_portal(user)
    elif user_role == "judge":
        render_judge_portal(user)
    elif user_role == "admin":
        render_admin_portal(user)
    else:
        st.error(f"Unrecognized role '{user_role}'. Contact System Administrator.")
