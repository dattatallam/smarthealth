"""All SQL lives here. Every query is parameterized (%s placeholders)."""
from backend.database.connection import db_cursor, DatabaseError
from backend.ml.features import DB_COLUMNS

_DB_TO_MODEL = {v: k for k, v in DB_COLUMNS.items()}


def create_user(full_name, email, password_hash):
    try:
        with db_cursor(commit=True) as cur:
            cur.execute("INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                        (full_name, email.lower(), password_hash))
            return cur.lastrowid
    except DatabaseError as exc:
        if str(exc) == "duplicate":
            raise DatabaseError("An account with this email already exists.") from exc
        raise


def get_user_by_email(email):
    with db_cursor() as cur:
        cur.execute("SELECT id, full_name, email, password_hash FROM users WHERE email = %s", (email.lower(),))
        return cur.fetchone()


def add_record(user_id, result) -> int:
    inputs = result["inputs"]
    cols = ["user_id", "chronological_age"] + list(DB_COLUMNS.values()) + \
           ["biological_age", "age_acceleration", "risk_points", "health_risk", "health_score", "top_driver"]
    vals = [user_id, inputs["chronological_age"]] + [inputs[k] for k in DB_COLUMNS] + \
           [result["biological_age"], result["age_acceleration"], result["risk"]["points"],
            result["risk"]["label"], result["risk"]["health_score"], result["top_driver"]]
    sql = f"INSERT INTO health_records ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
    with db_cursor(commit=True) as cur:
        cur.execute(sql, vals)
        return cur.lastrowid


def get_records(user_id, limit=100):
    with db_cursor() as cur:
        cur.execute("SELECT * FROM health_records WHERE user_id = %s ORDER BY created_at DESC, id DESC LIMIT %s",
                    (user_id, limit))
        return cur.fetchall()


def record_to_inputs(row) -> dict:
    """Rebuild the model-input dict from a database row."""
    inputs = {_DB_TO_MODEL[c]: row[c] for c in _DB_TO_MODEL}
    inputs["chronological_age"] = row["chronological_age"]
    return inputs
