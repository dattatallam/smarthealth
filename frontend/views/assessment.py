import streamlit as st
from backend.database import repository
from backend.database.connection import DatabaseError
from backend.ml.features import CHOICES
from backend.services.assessment_service import compute_result
from backend.services.alerts import send_alert, alerts_configured, AlertError, ALERT_LABELS
from frontend.components.ui import html
from backend.services.validation import validate_inputs


def _num(label, key, **kw):
    return st.number_input(label, value=None, key=key, **kw)


def render():
    html('<div class="sh-label">Step 1</div><div class="sh-h1">New assessment</div>'
         '<p class="sh-muted">Enter your latest health values. BMI is calculated automatically from height and weight.</p>')
    with st.form("assessment_form"):
        html('<div class="sh-label">Basics</div>')
        a, b = st.columns(2)
        age = a.number_input("Age (years)", value=None, placeholder="e.g. 35", key="f_age")
        gender = b.selectbox("Gender", CHOICES["Gender"], key="f_gender")
        html('<div class="sh-label" style="margin-top:.8rem">Body measurements</div>')
        c1, c2, c3, c4 = st.columns(4)
        wt = c1.number_input("Weight (kg)", value=None, key="f_wt")
        ht = c2.number_input("Height (cm)", value=None, key="f_ht")
        waist = c3.number_input("Waist (cm)", value=None, key="f_waist")
        pulse = c4.number_input("Resting pulse (bpm)", value=None, key="f_pulse")
        html('<div class="sh-label" style="margin-top:.8rem">Blood pressure</div>')
        d1, d2 = st.columns(2)
        sbp = d1.number_input("Systolic BP (mmHg)", value=None, key="f_sbp")
        dbp = d2.number_input("Diastolic BP (mmHg)", value=None, key="f_dbp")
        html('<div class="sh-label" style="margin-top:.8rem">Blood tests</div>')
        e1, e2, e3, e4, e5 = st.columns(5)
        chol = e1.number_input("Total cholesterol (mg/dL)", value=None, key="f_chol")
        hgb = e2.number_input("Hemoglobin (g/dL)", value=None, key="f_hgb")
        hct = e3.number_input("Hematocrit (%)", value=None, key="f_hct")
        cre = e4.number_input("Creatinine (mg/dL)", value=None, key="f_cre")
        uric = e5.number_input("Uric acid (mg/dL)", value=None, key="f_uric")
        html('<div class="sh-label" style="margin-top:.8rem">Lifestyle</div>')
        g1, g2, g3 = st.columns(3)
        smoke = g1.selectbox("Smoking", CHOICES["Smoking_Status"], key="f_smoke")
        sleep = g2.selectbox("Sleep", CHOICES["Sleep_Category"], index=2, key="f_sleep")
        act = g3.selectbox("Physical activity", CHOICES["Physical_Activity"], key="f_act")
        submit = st.form_submit_button("Run assessment →", type="primary")

    if not submit:
        return
    inputs = {"chronological_age": age, "Gender": gender, "BMXWT": wt, "BMXHT": ht, "BMXWAIST": waist,
              "BPXPLS": pulse, "Mean_Systolic_BP": sbp, "Mean_Diastolic_BP": dbp, "LBXTC": chol,
              "LBXHGB": hgb, "LBXHCT": hct, "LBXSCR": cre, "LBXSUA": uric,
              "Smoking_Status": smoke, "Sleep_Category": sleep, "Physical_Activity": act}
    errors = validate_inputs(inputs)
    if errors:
        for e in errors:
            st.error(e)
        return
    try:
        with st.spinner("Analysing your data…"):
            result = compute_result(inputs)
    except FileNotFoundError as exc:
        st.error(str(exc)); return
    except Exception as exc:
        st.error(f"Prediction failed: {exc}"); return
    try:
        result["record_id"] = repository.add_record(st.session_state.user["id"], result)
    except DatabaseError as exc:
        st.warning(f"Result calculated but NOT saved: {exc}")
    if result["risk"]["label"] in ALERT_LABELS and alerts_configured():
        try:
            user = st.session_state.user
            send_alert(user["email"], user["name"], result)
            st.session_state.flash = f"Alert email sent to {user['email']}."
        except AlertError as exc:
            st.session_state.flash = str(exc)
    st.session_state.current_result = result
    st.session_state.page = "results"
    st.rerun()
