"""One function that runs the whole flow: validate -> preprocess -> predict -> risk -> SHAP -> advice."""
from datetime import datetime
from backend.ml.preprocessing import add_bmi, build_input_frame
from backend.ml.prediction import predict_biological_age
from backend.services.risk import assess_risk
from backend.ml.shap_explainer import explain
from backend.services.recommendations import build_recommendations


def compute_result(inputs: dict) -> dict:
    inputs = add_bmi(inputs)
    chrono = float(inputs["chronological_age"])
    bio = round(predict_biological_age(build_input_frame(inputs)), 1)
    accel = round(bio - chrono, 1)          # age acceleration = predicted biological age - chronological age
    risk = assess_risk(inputs, accel)
    exp = explain(inputs)
    return {
        "inputs": inputs, "chronological_age": chrono, "biological_age": bio, "age_acceleration": accel,
        "risk": risk, "shap": exp, "recommendations": build_recommendations(inputs, risk, accel),
        "top_driver": str(exp["table"].iloc[0]["label"]), "created_at": datetime.now(), "record_id": None,
    }
