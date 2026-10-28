import os
import base64
import functools
import streamlit as st

_FONTS_DIR = os.path.join(os.path.dirname(__file__), "fonts")

@functools.lru_cache(maxsize=1)
def _get_base64_font(filename: str) -> str:
    p = os.path.join(_FONTS_DIR, filename)
    if os.path.exists(p):
        with open(p, "rb") as fp:
            return base64.b64encode(fp.read()).decode("utf-8")
    return ""

def _build_font_face_block(weight: int, filename: str, style_name: str) -> str:
    b64 = _get_base64_font(filename)
    b64_src = f", url('data:font/ttf;base64,{b64}') format('truetype')" if b64 else ""
    clean_map = {
        300: "TBJ-Cota-Sans-Light.ttf",
        400: "TBJ-Cota-Sans-Regular.ttf",
        500: "TBJ-Cota-Sans-Medium.ttf",
        600: "TBJ-Cota-Sans-SemiBold.ttf",
        700: "TBJ-Cota-Sans-Bold.ttf",
        800: "TBJ-Cota-Sans-ExtraBold.ttf"
    }
    clean_file = clean_map.get(weight, "TBJ-Cota-Sans-Regular.ttf")

    return f"""
    @font-face {{
        font-family: 'TBJ Cota Sans';
        src: local('TBJ Cota Sans Demo {style_name}'),
             local('TBJ Cota Sans {style_name}'),
             local('TBJCotaSansDemo-{style_name}'),
             local('TBJ Cota Sans'),
             local('TBJ Cota'),
             url('/app/static/fonts/{clean_file}') format('truetype')
             {b64_src};
        font-weight: {weight};
        font-style: normal;
        font-display: swap;
    }}
    @font-face {{
        font-family: 'TBJ Cota Sans Demo';
        src: local('TBJ Cota Sans Demo {style_name}'),
             local('TBJ Cota Sans {style_name}'),
             local('TBJCotaSansDemo-{style_name}'),
             url('/app/static/fonts/{clean_file}') format('truetype')
             {b64_src};
        font-weight: {weight};
        font-style: normal;
        font-display: swap;
    }}
    """

def apply_pristine_light_theme():
    """
    Enterprise Sovereign Forensic & Judicial Platform Theme.
    Built with the engineering aesthetic of Stripe, Linear, and Palantir:
    - Primary Typography: TBJ Cota Sans / TBJ Cota Sans Demo
    - Hashes & Terminal: JetBrains Mono
    - Icons: Google Material Symbols
    - Texture: Architectural micro-dot matrix background
    """
    font_faces = [
        _build_font_face_block(300, "TBJCotaSansDemo-Light-BF6a0401c841ca0.ttf", "Light"),
        _build_font_face_block(400, "TBJCotaSansDemo-Regular-BF6a0401c93bdd1.ttf", "Regular"),
        _build_font_face_block(500, "TBJCotaSansDemo-Medium-BF6a0401c874a39.ttf", "Medium"),
        _build_font_face_block(600, "TBJCotaSansDemo-SemiBold-BF6a0401c864183.ttf", "SemiBold"),
        _build_font_face_block(700, "TBJCotaSansDemo-Bold-BF6a0401c82a657.ttf", "Bold"),
        _build_font_face_block(800, "TBJCotaSansDemo-ExtraBold-BF6a0401c8543b5.ttf", "ExtraBold"),
    ]
    all_font_faces = "\n".join(font_faces)

    custom_css = f"""
    <style>
    /* 1. IMPORTS FIRST */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

    /* 2. TBJ COTA SANS FONT FACES */
    {all_font_faces}

    /* 3. BASE RESET & HIGH-TECH CANVAS */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #F8FAFC !important;
        background-image: radial-gradient(#CBD5E1 0.8px, transparent 0.8px) !important;
        background-size: 20px 20px !important;
        background-attachment: fixed !important;
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        color: #0F172A !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }}

    /* 4. TYPOGRAPHY TARGETING */
    h1, h2, h3, h4, h5, h6,
    p, label,
    .stTextInput input, .stTextArea textarea,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span:not([class*="material"]),
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span,
    [data-baseweb="select"] div,
    [data-baseweb="menu"] li,
    .forensic-card, .metric-card, .inst-badge,
    table, th, td {{
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', 'Inter', sans-serif !important;
    }}

    /* 5. MATERIAL SYMBOLS (PREVENTS TEXT LIGATURE CORRUPTION) */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {{
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
        font-style: normal !important;
        text-transform: none !important;
        letter-spacing: normal !important;
    }}

    /* 6. STREAMLIT EXPANDER ACCORDION */
    [data-testid="stExpander"] {{
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
        margin-top: 10px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    [data-testid="stExpander"]:hover {{
        border-color: #CBD5E1 !important;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05) !important;
    }}
    [data-testid="stExpander"] summary {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 12px 16px !important;
        background: #FFFFFF !important;
        cursor: pointer !important;
    }}
    [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 18px !important;
        min-width: 18px !important;
        max-width: 18px !important;
        height: 18px !important;
        overflow: hidden !important;
        flex-shrink: 0 !important;
    }}
    [data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {{
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.4 !important;
    }}
    [data-testid="stExpanderDetails"] {{
        padding: 14px 18px 18px 18px !important;
        background: #FFFFFF !important;
        border-top: 1px solid #F1F5F9 !important;
    }}

    /* 7. ALL INPUT FIELDS */
    input[type="text"], 
    input[type="password"], 
    textarea, 
    [data-baseweb="input"] input,
    .stTextInput input,
    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', sans-serif !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        padding: 9px 13px !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    input:focus, textarea:focus {{
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
        outline: none !important;
    }}

    /* 8. TABS */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #EEF2F6 !important;
        padding: 4px !important;
        border-radius: 10px !important;
        gap: 4px !important;
        border: 1px solid #E2E8F0 !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 7px !important;
        background-color: transparent !important;
        padding: 8px 18px !important;
        transition: all 0.15s ease !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] p, 
    .stTabs [data-baseweb="tab"] span {{
        color: #64748B !important;
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.08) !important;
    }}
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}

    /* 9. BUTTONS - ROBUST FULL-WIDTH ENTERPRISE STYLING */
    .stButton, .stButton > button {{
        width: 100% !important;
    }}
    .stButton > button {{
        font-family: 'TBJ Cota Sans', 'TBJ Cota Sans Demo', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border-radius: 8px !important;
        padding: 9px 12px !important;
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
    }}
    .stButton > button:hover {{
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
    }}
    .stButton > button[kind="primary"] {{
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
    }}

    /* 10. HASHES & TERMINAL CODE - JETBRAINS MONO */
    [data-testid="stCodeBlock"], pre, code, pre *, code *, .crypto-mono {{
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12.5px !important;
        background-color: #0B0F19 !important;
        color: #38BDF8 !important;
    }}

    /* 11. TELEMETRY BEACON */
    .telemetry-beacon {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px;
        font-weight: 600;
        color: #059669;
        letter-spacing: 0.02em;
    }}
    .telemetry-beacon * {{
        font-family: 'JetBrains Mono', monospace !important;
    }}
    .telemetry-beacon .dot {{
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
    }}
    </style>
    """
    if hasattr(st, "html"):
        st.html(custom_css)
    st.markdown(custom_css, unsafe_allow_html=True)
