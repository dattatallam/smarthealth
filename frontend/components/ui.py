"""Shared look & feel (CSS, logo, cards, navigation helper) matching the supplied Smart Health design."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: #F3FBFC; color: #0B1F33; color-scheme: light; }
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="base-input"], .stNumberInput input, .stTextInput input { background: #FFFFFF !important; color: #0B1F33 !important; }
[data-baseweb="input"], [data-baseweb="select"] > div { border: none !important; box-shadow: none !important; }
.stForm { background: #fff; border: 1px solid #E6EEF2 !important; border-radius: 16px; padding: 1.2rem; }
.stForm [data-testid="stNumberInput"] input,
.stForm [data-testid="stSelectbox"] [role="combobox"] {
  box-sizing: border-box; border: 1px solid #CBD5E1 !important; border-radius: 6px !important;
  background: #FFFFFF !important; box-shadow: none !important; outline: none !important;
}
.stForm [data-testid="stNumberInput"] input:focus,
.stForm [data-testid="stSelectbox"] [role="combobox"]:focus,
.stForm [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
.stForm [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
  border-color: #CBD5E1 !important; box-shadow: none !important; outline: none !important;
}
.stForm [data-testid="stNumberInput"]:focus-within,
.stForm [data-testid="stNumberInput"] :focus-within:not(input) {
  border: none !important; box-shadow: none !important; outline: none !important;
}
label, .stMarkdown p { color: #0B1F33; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { padding-top: 1.6rem; max-width: 1100px; }
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E6EEF2; }
[data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] .stButton > button { width: 100%; justify-content: flex-start; border: none; background: transparent;
  color: #3B4E60; font-weight: 500; border-radius: 10px; padding: .55rem .8rem; }
[data-testid="stSidebar"] .stButton > button:hover { background: #EEF6FA; color: #0B7BC0; }
[data-testid="stSidebar"] .stButton > button[kind="primary"] { background: #0B7BC0; color: #fff; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background: #0B7BC0; border: none; color: #fff;
  border-radius: 10px; font-weight: 600; padding: .55rem 1.1rem; }
.stButton > button[kind="secondary"], .stFormSubmitButton > button[kind="secondary"] { border-radius: 10px; border: 1px solid #E6EEF2; background: #fff; color: #0B1F33; font-weight: 600; }
.sh-logo { display:flex; align-items:center; gap:.5rem; font-weight:700; font-size:1.05rem; }
.sh-logo .dot { width:28px; height:28px; border-radius:8px; background:linear-gradient(135deg,#0B7BC0,#12B8A6); display:inline-flex; align-items:center; justify-content:center; color:#fff; font-size:.9rem; }
.sh-card { background:#fff; border:1px solid #E6EEF2; border-radius:16px; padding:1.1rem 1.3rem; box-shadow:0 1px 3px rgba(11,31,51,.04); margin-bottom:1rem; }
.sh-label { font-size:.68rem; letter-spacing:.08em; text-transform:uppercase; color:#6B7C8C; font-weight:600; }
.sh-big { font-size:2rem; font-weight:800; line-height:1.15; margin:.25rem 0; }
.sh-sub { font-size:.8rem; color:#6B7C8C; }
.sh-h1 { font-size:1.9rem; font-weight:800; margin:0; }
.sh-muted { color:#6B7C8C; font-size:.9rem; }
.sh-chip { display:inline-block; padding:.2rem .65rem; border-radius:999px; font-size:.72rem; font-weight:700; letter-spacing:.04em; background:#E3F7F4; color:#0E8F82; }
.sh-hero { font-size:3.1rem; font-weight:800; line-height:1.08; letter-spacing:-.02em; }
.sh-hero span { color:#12B8A6; }
.sh-bar-row { margin:.55rem 0; }
.sh-bar-top { display:flex; justify-content:space-between; font-size:.85rem; font-weight:500; }
.sh-bar-bg { background:#EAF1F5; border-radius:999px; height:9px; margin-top:.3rem; }
.sh-bar-fill { height:9px; border-radius:999px; }
.sh-rec { background:#fff; border:1px solid #E6EEF2; border-radius:16px; padding:1rem 1.3rem; margin-bottom:.8rem; }
.sh-rec p { margin:.5rem 0 0; }
.sh-auth-left { background:linear-gradient(145deg,#00A8D6 0%,#00CDBE 60%,#3DBE8B 100%); border-radius:18px; min-height:82vh; padding:1.6rem; color:#fff; display:flex; flex-direction:column; justify-content:space-between; }
.sh-disclaimer { font-size:.78rem; color:#6B7C8C; border-top:1px solid #E6EEF2; padding-top:.8rem; margin-top:1rem; }
.sh-row { display:flex; justify-content:space-between; align-items:center; padding:.6rem 0; border-bottom:1px solid #EEF3F6; font-size:.88rem; }
</style>
"""

HIDE_SIDEBAR = "<style>[data-testid='stSidebar'], [data-testid='collapsedControl'] {display:none;}</style>"


def html(s: str):
    """Render HTML safely in markdown (strips indentation so it is not treated as a code block)."""
    st.markdown("\n".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


def inject_css(hide_sidebar: bool):
    st.markdown(CSS, unsafe_allow_html=True)
    if hide_sidebar:
        st.markdown(HIDE_SIDEBAR, unsafe_allow_html=True)


def navigate(page: str):
    st.session_state.page = page


def logo(white=False):
    color = "#fff" if white else "#0B1F33"
    return f'<div class="sh-logo" style="color:{color}"><span class="dot">♥</span>Smart Health.</div>'


def stat_card(label, value, sub="", color="#0B1F33"):
    html(f'<div class="sh-card"><div class="sh-label">{label}</div>'
         f'<div class="sh-big" style="color:{color}">{value}</div><div class="sh-sub">{sub}</div></div>')


def bar_rows(items, max_abs=None, signed=False, unit=""):
    """items: list of (label, value). Draws horizontal bars like the 'feature importance' card."""
    max_abs = max_abs or max((abs(v) for _, v in items), default=1) or 1
    rows = ""
    for label, v in items:
        pct = max(2, abs(v) / max_abs * 100)
        color = ("#F59E0B" if v > 0 else "#12B8A6") if signed else "#0B7BC0"
        text = f"{v:+.2f}{unit}" if signed else f"{v:.1f}{unit}"
        rows += (f'<div class="sh-bar-row"><div class="sh-bar-top"><span>{label}</span><span>{text}</span></div>'
                 f'<div class="sh-bar-bg"><div class="sh-bar-fill" style="width:{pct:.0f}%;background:{color}"></div></div></div>')
    html(f'<div class="sh-card">{rows}</div>')
