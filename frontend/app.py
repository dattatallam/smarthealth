"""Smart Health Analytics - run from the project root with:  streamlit run frontend/app.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # project root, so "backend" can be imported

import streamlit as st
from frontend.components.ui import inject_css, navigate, logo, html

st.set_page_config(
    page_title="Smart Health",
    page_icon=str(Path(__file__).resolve().parent / "assets" / "health_logo.svg"),
    layout="wide",
    initial_sidebar_state="expanded",
)

ss = st.session_state
ss.setdefault("user", None)
ss.setdefault("page", "landing")

PUBLIC = {"landing", "login", "signup"}
if ss.user is None and ss.page not in PUBLIC:
    ss.page = "landing"
if ss.user is not None and ss.page in PUBLIC:
    ss.page = "assessment"
if ss.user is not None and ss.page == "dashboard":
    ss.page = "assessment"

inject_css(hide_sidebar=ss.user is None)

from frontend.views import landing, auth, assessment, results, history, about  # noqa: E402

NAV = [("assessment", "∿  New assessment"), ("results", "◎  Results"),
       ("history", "◷  History & trends"), ("about", "ⓘ  About project")]

if ss.user:
    with st.sidebar:
        html(logo())
        st.write("")
        for key, label in NAV:
            st.button(label, key=f"nav_{key}", on_click=navigate, args=(key,),
                      type="primary" if ss.page == key else "secondary", use_container_width=True)
        st.write("")
        html(f'<div class="sh-card" style="padding:.7rem"><div class="sh-sub">Signed in as</div><b style="font-size:.8rem">{ss.user["email"]}</b></div>')
        if st.button("Sign out", use_container_width=True):
            ss.clear()
            st.rerun()

ROUTES = {
    "landing": landing.render, "login": lambda: auth.render("login"), "signup": lambda: auth.render("signup"),
    "assessment": assessment.render, "results": results.render,
    "history": history.render, "about": about.render,
}
ROUTES[ss.page]()
