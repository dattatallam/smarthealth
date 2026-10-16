"""Loads the saved model ONCE and predicts biological age."""
from functools import lru_cache
import joblib
from backend.ml.features import MODEL_FILE, FEATURES_FILE, FEATURE_ORDER


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_FILE}. Put biological_age_model.pkl inside models/.")
    pipeline = joblib.load(MODEL_FILE)
    if FEATURES_FILE.exists():
        saved = list(joblib.load(FEATURES_FILE))
        if saved != FEATURE_ORDER:
            raise ValueError("Feature list in biological_age_features.pkl differs from backend/ml/features.py.")
    return pipeline


def predict_biological_age(frame) -> float:
    return float(load_model().predict(frame)[0])
