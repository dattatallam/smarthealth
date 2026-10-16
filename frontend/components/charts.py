"""Seaborn/Matplotlib charts drawn from the user's own saved records (clean, light theme)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BLUE, GREEN, AMBER, GRID = "#0B7BC0", "#12B8A6", "#F59E0B", "#E6EEF2"
RISK_ORDER = ["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"]


def _style(ax, title=None):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(axis="y", color=GRID)
    ax.tick_params(colors="#6B7C8C", labelsize=8)
    if title:
        ax.set_title(title, loc="left", fontsize=10, fontweight="bold", color="#0B1F33")


def _fig(h=3.0, w=6.4):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def trend_chart(df: pd.DataFrame):
    d = df.sort_values("created_at").reset_index(drop=True)
    d["Assessment"] = d.index + 1
    fig, ax = _fig(3.0)
    ax.plot(d["Assessment"], d["health_score"], marker="o", color=BLUE, label="Health score")
    ax.plot(d["Assessment"], d["risk_points"], marker="o", color=GREEN, label="Risk points")
    ax.set_ylim(0, 100); ax.set_xlabel("Assessment #", fontsize=8); ax.set_ylabel("")
    ax.set_xticks(d["Assessment"]); ax.legend(frameon=False, fontsize=8)
    _style(ax); fig.tight_layout()
    return fig


def bio_vs_chrono(df: pd.DataFrame):
    fig, ax = _fig(3.2, 4.2)
    lo = min(df["chronological_age"].min(), df["biological_age"].min()) - 3
    hi = max(df["chronological_age"].max(), df["biological_age"].max()) + 3
    ax.plot([lo, hi], [lo, hi], ls="--", color="#9FB3C2", lw=1)
    ax.scatter(df["chronological_age"], df["biological_age"], s=60, color=BLUE)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("Chronological age", fontsize=8); ax.set_ylabel("Biological age", fontsize=8)
    _style(ax, "Biological vs chronological age"); fig.tight_layout()
    return fig


def acceleration_chart(df: pd.DataFrame):
    fig, ax = _fig(3.2, 4.2)
    d = df.sort_values("created_at").reset_index(drop=True)
    ax.bar(d.index + 1, d["age_acceleration"], color=[AMBER if v > 0 else GREEN for v in d["age_acceleration"]])
    ax.axhline(0, color="#9FB3C2", lw=1)
    ax.set_xticks(d.index + 1)
    ax.set_xlabel("Assessment #", fontsize=8); ax.set_ylabel("Years", fontsize=8)
    _style(ax, "Age acceleration (years)"); fig.tight_layout()
    return fig


def risk_distribution(df: pd.DataFrame):
    fig, ax = _fig(3.0, 4.2)
    palette = {"Low Risk": GREEN, "Moderate Risk": "#7CC4E8", "High Risk": AMBER, "Very High Risk": "#E5484D"}
    counts = df["health_risk"].value_counts().reindex(RISK_ORDER, fill_value=0)
    ax.bar(RISK_ORDER, counts.values, color=[palette[risk] for risk in RISK_ORDER])
    ax.set_xlabel(""); ax.set_ylabel("Assessments", fontsize=8)
    ax.tick_params(axis="x", labelrotation=15)
    ax.yaxis.get_major_locator().set_params(integer=True)
    _style(ax, "Risk categories"); fig.tight_layout()
    return fig
