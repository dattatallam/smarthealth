"""MySQL connection. Credentials come from environment variables (.env) or Streamlit secrets - never from source code."""
import os
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class DatabaseError(Exception):
    """Safe, user-friendly database error (no credentials inside)."""


def _setting(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


def get_connection():
    try:
        return mysql.connector.connect(
            host=_setting("MYSQL_HOST", "localhost"),
            port=int(_setting("MYSQL_PORT", 3306)),
            user=_setting("MYSQL_USER"),
            password=_setting("MYSQL_PASSWORD"),
            database=_setting("MYSQL_DATABASE", "smart_health_analytics"),
            connection_timeout=8,
        )
    except Error as exc:
        raise DatabaseError("Cannot connect to the MySQL database. Check that MySQL Server is running and your .env settings are correct.") from exc


@contextmanager
def db_cursor(commit=False):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        yield cur
        if commit:
            conn.commit()
    except Error as exc:
        conn.rollback()
        if getattr(exc, "errno", None) == 1062:
            raise DatabaseError("duplicate") from exc
        raise DatabaseError("A database error occurred. Please try again.") from exc
    finally:
        conn.close()
