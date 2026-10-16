import streamlit as st
from backend.database import repository
from backend.database.connection import DatabaseError
from frontend.components.charts import trend_chart
from frontend.components.ui import html, stat_card, navigate
import pandas as pd
import matplotlib.pyplot as plt

RISK_COLOR = {"Low Risk": "#12B8A6", "Moderate Risk": "#0B7BC0", "High Risk": "#F59E0B", "Very High Risk": "#E5484D"}


def render():
    user = st.session_state.user
    h1, h2 = st.columns([4, 1])
    with h1:
        html(f'<div class="sh-label">Welcome back</div><div class="sh-h1">Hi, {user["name"].split()[0]} 👋</div>'
             '<p class="sh-muted">Here’s a snapshot of your latest health signals.</p>')
    h2.button("＋ New assessment", type="primary", on_click=navigate, args=("assessment",), use_container_width=True)

    try:
        rows = repository.get_records(user["id"])
    except DatabaseError as exc:
        st.error(str(exc)); return
    if not rows:
        html('<div class="sh-card"><b>No assessments yet.</b><p class="sh-muted">Run your first assessment to see your biological age, health score and explanations.</p></div>')
        return
    df = pd.DataFrame(rows)
    last = rows[0]
    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("Biological age", f'{last["biological_age"]:.0f}', f'vs {last["chronological_age"]:.0f} chronological', "#0B7BC0")
    with c2: stat_card("Health score", f'{last["health_score"]}/100', "Higher is better")
    with c3: stat_card("Health risk", last["health_risk"].replace(" Risk", ""), f'{last["risk_points"]} risk points', RISK_COLOR[last["health_risk"]])
    with c4: stat_card("Age acceleration", f'{last["age_acceleration"]:+.1f}', "years", "#E5484D" if last["age_acceleration"] > 0 else "#12B8A6")

    left, right = st.columns([2, 1])
    with left:
        html('<div class="sh-card"><b>Health score trend</b><div class="sh-sub">Your assessments over time</div></div>')
        fig = trend_chart(df)
        st.pyplot(fig, use_container_width=True); plt.close(fig)
    with right:
        html('<div class="sh-card"><b>Quick actions</b></div>')
        st.button("Run a new assessment", on_click=navigate, args=("assessment",), use_container_width=True)
        st.button("View full history", on_click=navigate, args=("history",), use_container_width=True)
        html(f'<div class="sh-card"><div class="sh-label">Top health driver</div><b>{last["top_driver"] or "–"}</b> — biggest influence on your latest estimate</div>')

    html('<div class="sh-card"><b>Previous predictions</b>' + "".join(
        f'<div class="sh-row"><span>Health score {r["health_score"]}/100 · Bio age {r["biological_age"]:.0f}</span>'
        f'<span class="sh-sub">{r["created_at"]:%d/%m/%Y, %H:%M}</span></div>' for r in rows[:3]) + '</div>')
