"""Builds the one-row DataFrame the saved pipeline expects.
Imputation + one-hot encoding are already inside the pickled pipeline, so we only
(1) compute BMI exactly as BMXBMI (kg / m^2) and (2) arrange columns in training order."""
import pandas as pd
from backend.ml.features import FEATURE_ORDER


def add_bmi(inputs: dict) -> dict:
    out = dict(inputs)
    out["BMXBMI"] = round(out["BMXWT"] / (out["BMXHT"] / 100) ** 2, 1)
    return out


def build_input_frame(inputs: dict) -> pd.DataFrame:
    inputs = add_bmi(inputs)
    return pd.DataFrame([{k: inputs[k] for k in FEATURE_ORDER}], columns=FEATURE_ORDER)
