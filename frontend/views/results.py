import streamlit as st
from backend.services.alerts import send_alert, AlertError
from frontend.components.ui import html, stat_card, bar_rows, navigate

RISK_COLOR = {"Low Risk": "#12B8A6", "Moderate Risk": "#0B7BC0", "High Risk": "#F59E0B", "Very High Risk": "#E5484D"}


def render():
    r = st.session_state.get("current_result")
    if not r:
        html('<div class="sh-h1">Results</div><p class="sh-muted">Run an assessment first.</p>')
        st.button("New assessment", type="primary", on_click=navigate, args=("assessment",))
        return
    accel = r["age_acceleration"]
    if st.session_state.get("flash"):
        st.info(st.session_state.pop("flash"))
    html(f'<div class="sh-label">Results · {r["created_at"]:%d %b %Y, %H:%M}</div><div class="sh-h1">Your results</div>')

    html('<h3 style="margin-top:1rem">A · Biological age prediction</h3>')
    c1, c2, c3 = st.columns(3)
    with c1: stat_card("Chronological age", f'{r["chronological_age"]:.0f} yrs', "Your actual age")
    with c2: stat_card("Predicted biological age", f'{r["biological_age"]:.1f} yrs', "XGBoost model estimate", "#0B7BC0")
    with c3: stat_card("Age acceleration", f"{accel:+.1f} yrs", "Biological − chronological",
                       "#E5484D" if accel > 0 else "#12B8A6")
    direction = "older" if accel > 0 else "younger"
    st.caption(f"The model estimates your body profile resembles that of someone about {abs(accel):.1f} years {direction} than your actual age. This is a statistical estimate, not a medical diagnosis.")

    risk = r["risk"]
    html('<h3 style="margin-top:1rem">B · Health risk assessment</h3>')
    color = RISK_COLOR[risk["label"]]
    html(f"""<div class="sh-card"><div class="sh-label">Overall wellness risk indicator</div>
    <div class="sh-big" style="color:{color}">{risk["label"]}</div>
    <div class="sh-sub">{risk["points"]} risk points out of 100 · Health score {risk["health_score"]}/100</div>
    <div class="sh-bar-bg" style="margin-top:.6rem"><div class="sh-bar-fill" style="width:{max(2, risk["points"])}%;background:{color}"></div></div>
    <div class="sh-sub" style="margin-top:.4rem">Low 0–19 · Moderate 20–39 · High 40–59 · Very High 60+</div></div>""")
    with st.expander("How this score was calculated"):
        rows = "".join(f'<div class="sh-row"><span>{b["factor"]} — {b["note"]}</span><b>{b["points"]}/{b["max"]}</b></div>' for b in risk["breakdown"])
        html(f'<div>{rows}</div>')
        st.caption("Rule-based points from public reference ranges, not a trained or clinically validated model.")

    html('<h3 style="margin-top:1rem">C · Explainable AI (SHAP)</h3>')
    t = r["shap"]["table"]
    top = t.head(8)
    st.caption("Years each factor pushed your biological-age estimate up (amber) or down (green). Computed by SHAP from the loaded model and your inputs.")
    bar_rows([(l, v) for l, v in zip(top["label"], top["shap_years"])], signed=True, unit=" yrs")

    html('<h3 style="margin-top:1rem">D · Recommendations</h3>')
    for cat, text in r["recommendations"]:
        html(f'<div class="sh-rec"><span class="sh-chip">{cat}</span><p>{text}</p></div>')
    html('<div class="sh-disclaimer">General wellness guidance only. It is not medical advice, diagnosis or treatment. '
         'For high-risk results or any health concern, consult a qualified healthcare professional.</div>')
    if st.button("✉ Email me this result", key="email_alert"):
        try:
            u = st.session_state.user
            send_alert(u["email"], u["name"], r)
            st.success(f"Email sent to {u['email']}.")
        except AlertError as exc:
            st.error(str(exc))
    if r.get("record_id") is None:
        st.warning("This result was not saved to the database.")
