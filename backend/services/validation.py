"""Input validation. Returns a list of readable error messages (empty list = valid)."""
import math

# key: (label, min, max, unit)
RANGES = {
    "chronological_age": ("Age", 18, 85, "years"),
    "BMXWT": ("Weight", 30, 250, "kg"),
    "BMXHT": ("Height", 120, 220, "cm"),
    "BMXWAIST": ("Waist circumference", 40, 200, "cm"),
    "BPXPLS": ("Resting pulse", 35, 200, "bpm"),
    "Mean_Systolic_BP": ("Systolic BP", 70, 250, "mmHg"),
    "Mean_Diastolic_BP": ("Diastolic BP", 40, 150, "mmHg"),
    "LBXTC": ("Total cholesterol", 80, 500, "mg/dL"),
    "LBXHGB": ("Hemoglobin", 5, 20, "g/dL"),
    "LBXHCT": ("Hematocrit", 15, 65, "%"),
    "LBXSCR": ("Creatinine", 0.2, 10, "mg/dL"),
    "LBXSUA": ("Uric acid", 1, 15, "mg/dL"),
}


def _missing(v):
    return v is None or (isinstance(v, float) and math.isnan(v))


def validate_inputs(inputs: dict) -> list:
    errors = []
    for key, (label, lo, hi, unit) in RANGES.items():
        v = inputs.get(key)
        if _missing(v):
            errors.append(f"{label} is required.")
        elif not (lo <= v <= hi):
            errors.append(f"{label} must be between {lo} and {hi} {unit} (you entered {v}).")
    for key in ("Gender", "Smoking_Status", "Sleep_Category", "Physical_Activity"):
        if not inputs.get(key):
            errors.append(f"{key.replace('_', ' ')} is required.")
    sys_, dia = inputs.get("Mean_Systolic_BP"), inputs.get("Mean_Diastolic_BP")
    if not _missing(sys_) and not _missing(dia) and sys_ <= dia:
        errors.append("Systolic BP must be higher than diastolic BP.")
    wt, ht = inputs.get("BMXWT"), inputs.get("BMXHT")
    if not _missing(wt) and not _missing(ht) and ht > 0:
        bmi = wt / (ht / 100) ** 2
        if not (12 <= bmi <= 70):
            errors.append(f"Calculated BMI ({bmi:.1f}) is outside the sensible range 12–70. Check height and weight.")
    return errors
