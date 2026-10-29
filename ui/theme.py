import streamlit as st

def apply_pristine_light_theme():
    """
    Enterprise Sovereign Forensic & Judicial Platform Theme.
    Built with the engineering aesthetic of Stripe, Linear, and Palantir:
    - Primary Font: Inter (International Enterprise Standard - Ultra-Crisp, High-Legibility)
    - Code & Cryptographic Font: JetBrains Mono (Hashes, Signatures, Terminal Data)
    - Palette: Obsidian Deep Slate (#0B0F19), Crisp Surface White (#FFFFFF), Cobalt (#2563EB)
    - Texture: Architectural micro-dot matrix engineering canvas
    - Full containment cards, hairline borders, zero clutter.
    """
    custom_css = """
    <style>
    /* 1. GOOGLE FONTS IMPORTS (INTER & JETBRAINS MONO) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

    /* 2. BASE RESET & HIGH-TECH MICRO-DOT MESH CANVAS */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
        background-image: radial-gradient(#CBD5E1 0.85px, transparent 0.85px) !important;
        background-size: 20px 20px !important;
        background-attachment: fixed !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #0F172A !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }

    /* 3. UNIVERSAL HIGH-PRECISION TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6,
    p, label,
    .stTextInput input, .stTextArea textarea,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span:not([class*="material"]),
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    [data-baseweb="select"] div,
    [data-baseweb="menu"] li,
    table, th, td {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: -0.015em !important;
    }

    /* 4. ALL FORM WIDGET LABELS */
    label, 
    [data-testid="stWidgetLabel"], 
    [data-testid="stWidgetLabel"] p, 
    [data-testid="stWidgetLabel"] span {
        color: #334155 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 6px !important;
    }

    /* 5. ENTERPRISE COMMAND BANNER (.enterprise-header) */
    .enterprise-header {
        background: #0B0F19 !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 22px 26px !important;
        margin-bottom: 20px !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 20px -2px rgba(11, 15, 25, 0.25) !important;
    }
    .enterprise-header h1 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        margin: 10px 0 6px 0 !important;
        letter-spacing: -0.03em !important;
    }
    .enterprise-header p {
        color: #94A3B8 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        margin: 0 !important;
    }
    .enterprise-header code {
        background: #1E293B !important;
        color: #38BDF8 !important;
        padding: 3px 8px !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        border: 1px solid #334155 !important;
    }

    /* 6. OPERATIONAL METRIC CARDS (.metric-card) */
    .metric-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 18px 22px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    .metric-card:hover {
        border-color: #CBD5E1 !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
        transform: translateY(-1px) !important;
    }
    .metric-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 11.5px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        color: #64748B !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 2px !important;
    }
    .metric-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin: 4px 0 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.1 !important;
    }
    .metric-sub {
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        color: #059669 !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        gap: 5px !important;
    }

    /* 7. INSTITUTIONAL FORENSIC DOSSIER CARDS (.forensic-card) */
    .forensic-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 22px 24px !important;
        margin-bottom: 18px !important;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04) !important;
    }
    .forensic-card h3 {
        font-family: 'Inter', sans-serif !important;
        font-size: 16.5px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: -0.02em !important;
    }
    .forensic-card p {
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        color: #64748B !important;
        margin: 0 !important;
        line-height: 1.55 !important;
    }

    /* 8. INSTITUTIONAL BADGES (.inst-badge) */
    .inst-badge {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 4px 10px !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        border: 1px solid #E2E8F0 !important;
    }
    .inst-badge.police { background: #EFF6FF !important; color: #1D4ED8 !important; border-color: #BFDBFE !important; }
    .inst-badge.lawyer { background: #EEF2FF !important; color: #4338CA !important; border-color: #C7D2FE !important; }
    .inst-badge.judge { background: #FEF2F2 !important; color: #991B1B !important; border-color: #FECACA !important; }
    .inst-badge.admin { background: #F0FDF4 !important; color: #166534 !important; border-color: #BBF7D0 !important; }

    /* 9. TELEMETRY STATUS BEACON */
    .telemetry-beacon {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        background: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        padding: 4px 10px !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #059669 !important;
        letter-spacing: 0.02em !important;
    }
    .telemetry-beacon * {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .telemetry-beacon .dot {
        width: 6px !important;
        height: 6px !important;
        background-color: #10B981 !important;
        border-radius: 50% !important;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.6) !important;
    }

    /* 10. PROTECT ALL MATERIAL SYMBOLS & CHEVRON ICONS */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
        font-style: normal !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }

    /* 11. STREAMLIT EXPANDER ACCORDION - ZERO OVERLAP */
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
        margin-top: 10px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: #CBD5E1 !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05) !important;
    }
    [data-testid="stExpander"] summary {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 12px 16px !important;
        background: #FFFFFF !important;
        cursor: pointer !important;
    }
    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 18px !important;
        min-width: 18px !important;
        max-width: 18px !important;
        height: 18px !important;
        overflow: hidden !important;
        flex-shrink: 0 !important;
    }
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.4 !important;
    }
    [data-testid="stExpanderDetails"] {
        padding: 14px 18px 18px 18px !important;
        background: #FFFFFF !important;
        border-top: 1px solid #F1F5F9 !important;
    }

    /* 12. INPUT FIELDS & SELECTBOXES */
    input[type="text"], 
    input[type="password"], 
    textarea, 
    [data-baseweb="input"] input,
    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        padding: 9px 13px !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    input:focus, textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
        outline: none !important;
    }
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        transition: border-color 0.15s ease !important;
    }
    [data-baseweb="select"] > div:hover {
        border-color: #2563EB !important;
    }

    /* 13. TABS - SLEEK SEGMENTED CONTROL */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #EEF2F6 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        gap: 4px !important;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 16px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px !important;
        background-color: transparent !important;
        padding: 8px 18px !important;
        transition: all 0.15s ease !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] span {
        color: #64748B !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08) !important;
    }
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {
        color: #0F172A !important;
        font-weight: 700 !important;
    }

    /* 14. BUTTONS - ENTERPRISE STYLING */
    .stButton, .stButton > button {
        width: 100% !important;
    }
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        border-radius: 8px !important;
        padding: 9px 16px !important;
        min-height: 40px !important;
        height: auto !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }
    .stButton > button[kind="primary"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
    }

    /* 15. HASHES & TERMINAL CODE - JETBRAINS MONO */
    [data-testid="stCodeBlock"], pre, code, pre *, code *, .crypto-mono {
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12.5px !important;
        background-color: #0B0F19 !important;
        color: #38BDF8 !important;
    }

    /* 16. DATA TABLES */
    [data-testid="stDataFrame"], table {
        border-radius: 8px !important;
        overflow: hidden !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 13px !important;
    }
    table th {
        background: #F8FAFC !important;
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 0.04em !important;
        border-bottom: 1px solid #E2E8F0 !important;
        padding: 10px 14px !important;
    }
    table td {
        color: #1E293B !important;
        border-bottom: 1px solid #F1F5F9 !important;
        padding: 9px 14px !important;
    }

    /* 17. NATIVE STREAMLIT BORDERED CONTAINERS & METRIC CARDS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
        padding: 18px 22px !important;
        margin-bottom: 16px !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: transparent !important;
    }
    /* Metric tiles inside columns */
    [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 14px 18px !important;
        margin-bottom: 8px !important;
        min-height: 104px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #94A3B8 !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """
    if hasattr(st, "html"):
        st.html(custom_css)
    st.markdown(custom_css, unsafe_allow_html=True)
