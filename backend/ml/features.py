"""Feature definitions read from the trained pipeline (biological_age_model.pkl).
Order and category names MUST match what the model was trained with."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent   # backend/ml
MODEL_FILE = BASE_DIR / "models" / "biological_age_model.pkl"          # final model: sklearn Pipeline (imputer + one-hot + XGBRegressor)
FEATURES_FILE = BASE_DIR / "models" / "biological_age_features.pkl"    # list of the 16 raw input features
RF_FILE = BASE_DIR / "models" / "biological_age_random_forest.pkl"     # comparison model (19 features, not served in the UI)

NUMERIC_FEATURES = ["BMXBMI", "BMXWT", "BMXHT", "BMXWAIST", "BPXPLS", "Mean_Systolic_BP",
                    "Mean_Diastolic_BP", "LBXTC", "LBXHGB", "LBXHCT", "LBXSCR", "LBXSUA"]
CATEGORICAL_FEATURES = ["Gender", "Smoking_Status", "Sleep_Category", "Physical_Activity"]
FEATURE_ORDER = NUMERIC_FEATURES + CATEGORICAL_FEATURES

CHOICES = {
    "Gender": ["Female", "Male"],
    "Smoking_Status": ["Not at all", "Some days", "Every day"],
    "Sleep_Category": ["Less than 5 hours", "5–7 hours", "7–8 hours", "More than 8 hours"],
    "Physical_Activity": ["Sedentary", "Lightly Active", "Moderately Active", "Highly Active"],
}

LABELS = {
    "BMXBMI": "BMI", "BMXWT": "Weight", "BMXHT": "Height", "BMXWAIST": "Waist circumference",
    "BPXPLS": "Resting pulse", "Mean_Systolic_BP": "Systolic BP", "Mean_Diastolic_BP": "Diastolic BP",
    "LBXTC": "Total cholesterol", "LBXHGB": "Hemoglobin", "LBXHCT": "Hematocrit",
    "LBXSCR": "Creatinine", "LBXSUA": "Uric acid", "Gender": "Gender",
    "Smoking_Status": "Smoking", "Sleep_Category": "Sleep", "Physical_Activity": "Physical activity",
}

# model feature name -> database column
DB_COLUMNS = {
    "Gender": "gender", "BMXWT": "weight_kg", "BMXHT": "height_cm", "BMXBMI": "bmi",
    "BMXWAIST": "waist_cm", "BPXPLS": "pulse", "Mean_Systolic_BP": "systolic_bp",
    "Mean_Diastolic_BP": "diastolic_bp", "LBXTC": "total_cholesterol", "LBXHGB": "hemoglobin",
    "LBXHCT": "hematocrit", "LBXSCR": "creatinine", "LBXSUA": "uric_acid",
    "Smoking_Status": "smoking_status", "Sleep_Category": "sleep_category",
    "Physical_Activity": "physical_activity",
}
