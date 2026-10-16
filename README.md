# Smart Health Analytics
Machine Learning-Based Smart Health Analytics for Biological Age and Health Risk Prediction with Explainable AI.
Not a medical diagnosis tool.

## Structure: frontend and backend are separate
```
smart_health_analytics/
├── frontend/                    # everything the user SEES (Streamlit)
│   ├── app.py                   # entry point, sidebar, routing, login gate
│   ├── views/                   # landing, auth (login/register), dashboard, assessment, results, history, about
│   └── components/              # ui.py (white theme CSS, cards), charts.py (Seaborn)
├── backend/                     # everything the user does NOT see
│   ├── database/                # connection.py, repository.py (all SQL), sql/ (Workbench scripts)
│   ├── ml/                      # features.py, preprocessing.py, prediction.py, shap_explainer.py, models/*.pkl
│   └── services/                # assessment_service.py, risk.py, recommendations.py, validation.py, alerts.py, auth.py
├── .streamlit/                  # config.toml (light theme), secrets.toml.example
├── requirements.txt  .env.example  .gitignore  README.md
```
Rule: the frontend only calls backend services/repository; the backend never imports Streamlit UI code.

## Install
```
python -m venv venv
venv\Scripts\activate          (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
```

## MySQL
1. In MySQL Workbench run `backend/database/sql/01_create_database.sql`, then `02_create_tables.sql`.
2. Copy `.env.example` to `.env` (project root) and fill in MYSQL_* values (and SMTP_* for email alerts).

## Run (from the project root)
```
streamlit run frontend/app.py
```

## Model files (backend/ml/models/)
`biological_age_model.pkl` (final XGBoost pipeline), `biological_age_features.pkl` (16 features, checked at startup),
`biological_age_random_forest.pkl` (comparison model with different 19 features; not used by the form).

## How it works
Frontend form -> `backend.services.validation` -> `assessment_service.compute_result` (preprocess -> XGBoost prediction -> age acceleration ->
rule-based risk -> SHAP) -> `repository.add_record` (MySQL) -> results page. Age acceleration = predicted biological age − chronological age.

## SHAP
`shap.TreeExplainer` on the loaded XGBoost model; one-hot columns are summed back to the original feature.

## Health-risk methodology
Rule-based points score (`backend/services/risk.py`): BMI, waist, blood pressure, cholesterol, pulse, hemoglobin, creatinine, uric acid, smoking, sleep,
activity, age acceleration. Points 0–19 Low, 20–39 Moderate, 40–59 High, 60+ Very High. Educational, not clinically validated.

## Email alerts
Set SMTP_* in `.env` (Gmail needs an App Password). High / Very High Risk sends an email to the account address; the Results page also has an "Email me this result" button.
