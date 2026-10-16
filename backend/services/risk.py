"""Health-risk assessment (RULE-BASED, not a trained model).

No risk model exists in the supplied .pkl files, so this is a transparent points score
built from common public-health reference ranges (WHO BMI, AHA blood pressure, standard
cholesterol bands, etc). Each factor adds points; total points -> category.
It is an educational wellness indicator, NOT a diagnosis and NOT clinically validated.
See README section 'Health-risk methodology'."""

MAX_POINTS = 100
CATEGORIES = [(0, 19, "Low Risk"), (20, 39, "Moderate Risk"), (40, 59, "High Risk"), (60, 10**6, "Very High Risk")]


def _bmi(v):
    if v >= 35: return 15, "BMI 35 or above"
    if v >= 30: return 10, "BMI 30–34.9"
    if v >= 25: return 5, "BMI 25–29.9"
    if v < 18.5: return 5, "BMI below 18.5"
    return 0, "BMI in the 18.5–24.9 range"


def _waist(v, male):
    hi, mid = (102, 94) if male else (88, 80)
    if v > hi: return 8, "Waist well above reference"
    if v > mid: return 4, "Waist slightly above reference"
    return 0, "Waist within reference"


def _bp(s, d):
    if s >= 180 or d >= 120: return 18, "BP in a very high range"
    if s >= 140 or d >= 90: return 14, "BP 140/90 or above"
    if s >= 130 or d >= 80: return 8, "BP 130–139 / 80–89"
    if s >= 120: return 4, "BP slightly elevated"
    return 0, "BP below 120/80"


def _chol(v):
    if v >= 240: return 10, "Cholesterol 240 or above"
    if v >= 200: return 5, "Cholesterol 200–239"
    return 0, "Cholesterol below 200"


def _pulse(v):
    return (0, "Pulse 60–100 bpm") if 60 <= v <= 100 else (4, "Pulse outside 60–100 bpm")


def _hgb(v, male):
    lo, hi = (13.0, 17.5) if male else (12.0, 15.5)
    return (0, "Hemoglobin within reference") if lo <= v <= hi else (4, "Hemoglobin outside reference")


def _creat(v, male):
    lo, hi = (0.74, 1.35) if male else (0.59, 1.04)
    return (0, "Creatinine within reference") if lo <= v <= hi else (6, "Creatinine outside reference")


def _uric(v, male):
    return (4, "Uric acid above reference") if v > (7.2 if male else 6.0) else (0, "Uric acid within reference")


SMOKING = {"Every day": (12, "Smokes every day"), "Some days": (7, "Smokes some days"), "Not at all": (0, "Non-smoker")}
SLEEP = {"Less than 5 hours": (8, "Under 5 hours of sleep"), "5–7 hours": (3, "5–7 hours of sleep"),
         "7–8 hours": (0, "7–8 hours of sleep"), "More than 8 hours": (3, "Over 8 hours of sleep")}
ACTIVITY = {"Sedentary": (10, "Sedentary"), "Lightly Active": (5, "Lightly active"),
            "Moderately Active": (2, "Moderately active"), "Highly Active": (0, "Highly active")}


def _accel(a):
    if a > 5: return 10, "Biological age more than 5 years above actual"
    if a > 2: return 6, "Biological age 2–5 years above actual"
    if a > 0: return 2, "Biological age slightly above actual"
    return 0, "Biological age at or below actual"


def assess_risk(inputs: dict, age_acceleration: float) -> dict:
    male = inputs["Gender"] == "Male"
    parts = [
        ("BMI", 15, *_bmi(inputs["BMXBMI"])),
        ("Waist circumference", 8, *_waist(inputs["BMXWAIST"], male)),
        ("Blood pressure", 18, *_bp(inputs["Mean_Systolic_BP"], inputs["Mean_Diastolic_BP"])),
        ("Total cholesterol", 10, *_chol(inputs["LBXTC"])),
        ("Resting pulse", 4, *_pulse(inputs["BPXPLS"])),
        ("Hemoglobin", 4, *_hgb(inputs["LBXHGB"], male)),
        ("Creatinine", 6, *_creat(inputs["LBXSCR"], male)),
        ("Uric acid", 4, *_uric(inputs["LBXSUA"], male)),
        ("Smoking", 12, *SMOKING[inputs["Smoking_Status"]]),
        ("Sleep", 8, *SLEEP[inputs["Sleep_Category"]]),
        ("Physical activity", 10, *ACTIVITY[inputs["Physical_Activity"]]),
        ("Age acceleration", 10, *_accel(age_acceleration)),
    ]
    breakdown = [{"factor": f, "points": p, "max": m, "note": n} for f, m, p, n in parts]
    total = min(MAX_POINTS, sum(b["points"] for b in breakdown))
    label = next(name for lo, hi, name in CATEGORIES if lo <= total <= hi)
    return {"points": total, "label": label, "health_score": MAX_POINTS - total, "breakdown": breakdown}
