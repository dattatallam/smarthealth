"""Email alerts through SMTP (Gmail, Outlook, etc). Credentials come from .env / Streamlit secrets only."""
import smtplib
import ssl
from email.message import EmailMessage
from backend.database.connection import _setting

ALERT_LABELS = ("High Risk", "Very High Risk")


class AlertError(Exception):
    pass


def alerts_configured() -> bool:
    return all(_setting(k) for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD"))


def build_message(to_email: str, name: str, result: dict) -> EmailMessage:
    risk = result["risk"]
    top = ", ".join(result["shap"]["table"].head(3)["label"])
    msg = EmailMessage()
    msg["Subject"] = f"Smart Health alert: {risk['label']} in your latest assessment"
    msg["From"] = _setting("ALERT_FROM") or _setting("SMTP_USER")
    msg["To"] = to_email
    msg.set_content(
        f"Hi {name},\n\n"
        f"Your latest Smart Health assessment shows a {risk['label']} wellness indicator "
        f"({risk['points']}/100 risk points, health score {risk['health_score']}/100).\n"
        f"Chronological age: {result['chronological_age']:.0f} | Estimated biological age: {result['biological_age']:.1f} "
        f"| Age acceleration: {result['age_acceleration']:+.1f} years.\n"
        f"Main factors in the estimate: {top}.\n\n"
        "Please consider consulting a qualified healthcare professional to review these values.\n"
        "If you feel unwell or think this is an emergency, call your local emergency number immediately.\n\n"
        "This is an automated educational wellness message, not a medical diagnosis. "
        "Smart Health cannot monitor you continuously or contact emergency services."
    )
    return msg


def send_alert(to_email: str, name: str, result: dict) -> None:
    if not alerts_configured():
        raise AlertError("Email alerts are not configured. Add the SMTP_* settings to your .env file.")
    msg = build_message(to_email, name, result)
    host, port = _setting("SMTP_HOST"), int(_setting("SMTP_PORT", 587))
    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(_setting("SMTP_USER"), _setting("SMTP_PASSWORD"))
            server.send_message(msg)
    except (smtplib.SMTPException, OSError) as exc:
        raise AlertError("The alert email could not be sent. Check your SMTP settings and internet connection.") from exc
