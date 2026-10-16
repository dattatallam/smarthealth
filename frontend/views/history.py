import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from backend.database import repository
from backend.database.connection import DatabaseError
from frontend.components import charts
from backend.services.assessment_service import compute_result
from frontend.components.ui import html, bar_rows, navigate


@st.cache_data(show_spinner=False)
def _importance(inputs_list):
    from backend.ml.shap_explainer import explain
    totals = {}
    for inp in inputs_list:
        t = explain(inp)["table"]
        for l, a in zip(t["label"], t["abs"]):
            totals.setdefault(l, []).append(a)
    return sorted(((l, float(np.mean(v))) for l, v in totals.items()), key=lambda x: -x[1])


def render():
    html('<div class="sh-h1">History &amp; trends</div><p class="sh-muted">Everything you have saved in the MySQL database.</p>')
    try:
        rows = repository.get_records(st.session_state.user["id"])
    except DatabaseError as exc:
        st.error(str(exc)); return
    if not rows:
        st.info("No saved assessments yet."); return
    df = pd.DataFrame(rows)

    html('<div class="sh-card"><b>Saved assessments</b></div>')
    for r in rows[:15]:
        a, b = st.columns([5, 1])
        a.markdown(f'**{r["created_at"]:%d %b %Y, %H:%M}** — Bio age {r["biological_age"]:.1f} (actual {r["chronological_age"]:.0f}, {r["age_acceleration"]:+.1f}) · {r["health_risk"]} · score {r["health_score"]}/100')
        if b.button("View", key=f'view_{r["id"]}'):
            try:
                res = compute_result(repository.record_to_inputs(r))
                res["record_id"] = r["id"]
                res["created_at"] = r["created_at"]
                st.session_state.current_result = res
                st.session_state.page = "results"
                st.rerun()
            except Exception as exc:
                st.error(f"Could not open record: {exc}")

    c1, c2, c3 = st.columns(3)
    for col, fn in zip((c1, c2, c3), (charts.bio_vs_chrono, charts.acceleration_chart, charts.risk_distribution)):
        with col:
            fig = fn(df); st.pyplot(fig, use_container_width=True); plt.close(fig)

    html('<h3>Feature importance across your assessments</h3>')
    st.caption("Average absolute SHAP impact (years) over your latest assessments. Larger bars = more influence.")
    try:
        imp = _importance([repository.record_to_inputs(r) for r in rows[:20]])
        bar_rows(imp[:10], unit=" yrs")
    except Exception as exc:
        st.info(f"Feature importance unavailable: {exc}")
