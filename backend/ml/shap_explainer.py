"""SHAP explanation computed from the real loaded model and the user's real input."""
from functools import lru_cache
import numpy as np
import pandas as pd
import shap
from backend.ml.features import CATEGORICAL_FEATURES, LABELS
from backend.ml.prediction import load_model
from backend.ml.preprocessing import build_input_frame


@lru_cache(maxsize=1)
def _explainer():
    return shap.TreeExplainer(load_model().named_steps["model"])


def _raw_feature(encoded_name: str) -> str:
    """'numeric__BMXBMI' -> 'BMXBMI'; 'categorical__Gender_Male' -> 'Gender'."""
    name = encoded_name.split("__", 1)[1]
    for col in CATEGORICAL_FEATURES:
        if name.startswith(col + "_"):
            return col
    return name


def explain(inputs: dict) -> dict:
    """Returns SHAP values summed per ORIGINAL feature (one-hot columns are additive, so summing is exact)."""
    frame = build_input_frame(inputs)
    pipe = load_model()
    pre = pipe.named_steps["preprocessor"]
    X = pre.transform(frame)
    X = X.toarray() if hasattr(X, "toarray") else np.asarray(X)
    values = np.asarray(_explainer().shap_values(X))[0]
    grouped = {}
    for name, v in zip(pre.get_feature_names_out(), values):
        key = _raw_feature(name)
        grouped[key] = grouped.get(key, 0.0) + float(v)
    base = float(np.ravel(_explainer().expected_value)[0])
    table = pd.DataFrame({
        "feature": list(grouped),
        "label": [LABELS[k] for k in grouped],
        "value": [frame.iloc[0][k] for k in grouped],
        "shap_years": list(grouped.values()),
    })
    table["abs"] = table["shap_years"].abs()
    table = table.sort_values("abs", ascending=False).reset_index(drop=True)
    return {"table": table, "base_value": base}


def waterfall_figure(exp: dict, max_display: int = 10):
    """SHAP waterfall plot built from the grouped SHAP values."""
    import matplotlib.pyplot as plt
    t = exp["table"]
    names = [f"{l} = {v:.1f}" if isinstance(v, (int, float, np.floating)) else f"{l} = {v}"
             for l, v in zip(t["label"], t["value"])]
    explanation = shap.Explanation(values=t["shap_years"].to_numpy(), base_values=exp["base_value"],
                                   feature_names=names)
    plt.figure(figsize=(7, 4.5))
    shap.plots.waterfall(explanation, max_display=max_display, show=False)
    fig = plt.gcf()
    fig.tight_layout()
    return fig
