import streamlit as st
from frontend.components.ui import html, logo, navigate


def render():
    c1, c2, c3 = st.columns([5, 1, 1.3])
    with c1:
        html(logo())
    c2.button("Login", key="top_login", on_click=navigate, args=("login",), use_container_width=True)
    c3.button("Get started", key="top_signup", type="primary", on_click=navigate, args=("signup",), use_container_width=True)

    st.write("")
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        html('<span class="sh-chip">AI + Explainable ML for health</span>')
        html('<div class="sh-hero">Know your <span>biological age</span> before your birthday tells you.</div>')
        html('<p class="sh-muted" style="margin-top:1rem">Enter simple health metrics and get a transparent biological-age estimate, '
             'a wellness risk indicator, SHAP explanations and personalized lifestyle tips you can act on today.</p>')
        b1, b2, _ = st.columns([2, 1, 1])
        b1.button("Start free assessment →", key="hero_start", type="primary", on_click=navigate, args=("signup",), use_container_width=True)
        b2.button("Login", key="hero_login", on_click=navigate, args=("login",), use_container_width=True)
        html('<p class="sh-sub">🔒 Private account &nbsp;&nbsp; ✨ Explainable AI</p>')
    with right:
        html("""<div class="sh-card" style="margin-top:1rem">
        <div class="sh-label">Illustrative example</div>
        <div class="sh-big" style="color:#0B7BC0">28<span style="font-size:1rem;color:#6B7C8C">/34 yrs</span></div>
        <div class="sh-sub">Biological age vs chronological age</div>
        <div class="sh-bar-row"><div class="sh-bar-top"><span>Physical activity</span><span>−1.9 yrs</span></div>
        <div class="sh-bar-bg"><div class="sh-bar-fill" style="width:70%;background:#12B8A6"></div></div></div>
        <div class="sh-bar-row"><div class="sh-bar-top"><span>BMI</span><span>+0.8 yrs</span></div>
        <div class="sh-bar-bg"><div class="sh-bar-fill" style="width:35%;background:#F59E0B"></div></div></div>
        <div class="sh-sub" style="margin-top:.6rem">Sample only – your real results come from the trained model.</div></div>""")

    f1, f2, f3 = st.columns(3)
    for col, (t, d) in zip((f1, f2, f3), [
        ("Biological age", "XGBoost model trained on health measurements estimates your biological age."),
        ("Explainable AI", "SHAP shows which factors pushed your estimate up or down."),
        ("Health risk", "A transparent points-based wellness indicator: Low to Very High."),
    ]):
        with col:
            html(f'<div class="sh-card"><b>{t}</b><p class="sh-muted">{d}</p></div>')
    html('<div class="sh-disclaimer">Smart Health is an educational project. Results are estimates and not a medical diagnosis.</div>')
