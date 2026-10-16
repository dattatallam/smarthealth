from frontend.components.ui import html


def render():
    html("""<div class="sh-h1">About this project</div>
    <div class="sh-card" style="margin-top:1rem"><b>Machine Learning-Based Smart Health Analytics for Biological Age and Health Risk Prediction with Explainable AI</b>
    <p class="sh-muted">Built with Python, Pandas, NumPy, Scikit-learn, XGBoost, Random Forest, SHAP, Matplotlib, Seaborn, Streamlit and MySQL.</p></div>
    <div class="sh-card"><b>How it works</b>
    <p class="sh-muted">1) You enter 16 health values + age → 2) inputs are validated → 3) the saved scikit-learn pipeline (median/most-frequent imputation + one-hot encoding) prepares them →
    4) the saved XGBoost regressor predicts biological age → 5) age acceleration = biological − chronological → 6) a rule-based points score gives the wellness risk category →
    7) SHAP TreeExplainer explains the prediction → 8) the result is saved in external MySQL.</p></div>
    <div class="sh-card"><b>Models</b>
    <p class="sh-muted">Final model: XGBoost pipeline (biological_age_model.pkl). A Random Forest (biological_age_random_forest.pkl) was trained as a comparison model on a different 19-feature set (includes ethnicity and complete blood count), so it is kept in models/ but not used by this form.</p></div>
    <div class="sh-card"><b>Health risk</b><p class="sh-muted">The risk category is a transparent rule-based points score from public reference ranges. It is not a trained model, not clinically validated, and not a diagnosis.</p></div>
    <div class="sh-disclaimer">Educational project. Not a medical device. Consult a qualified healthcare professional for medical decisions.</div>""")
