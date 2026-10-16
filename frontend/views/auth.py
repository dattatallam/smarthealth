import streamlit as st
from backend.database import repository
from backend.database.connection import DatabaseError
from backend.services.auth import hash_password, verify_password, valid_email
from frontend.components.ui import html, logo, navigate


def _left():
    html(f"""<div class="sh-auth-left">{logo(white=True)}
    <div><div style="font-size:1.15rem;font-weight:600;line-height:1.4">“Understanding <i>why</i> a risk score changed is what turned my results into real habits.”</div>
    <div style="font-size:.75rem;opacity:.85;margin-top:.6rem">— Explainable AI in action</div></div></div>""")


def render(mode: str):
    left, right = st.columns(2, gap="small")
    with left:
        _left()
    with right:
        st.write("")
        st.write("")
        if mode == "login":
            html('<div class="sh-h1" style="font-size:1.5rem">Welcome back</div><p class="sh-muted">Sign in to view your health dashboard.</p>')
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                ok = st.form_submit_button("Sign in", type="primary", use_container_width=True)
            if ok:
                try:
                    user = repository.get_user_by_email(email.strip()) if valid_email(email.strip()) else None
                except DatabaseError as exc:
                    st.error(str(exc)); return
                if user and verify_password(password, user["password_hash"]):
                    st.session_state.user = {"id": user["id"], "name": user["full_name"], "email": user["email"]}
                    st.session_state.page = "dashboard"
                    st.rerun()
                st.error("Incorrect email or password.")
            st.button("New here? Create account", on_click=navigate, args=("signup",), key="to_signup")
        else:
            html('<div class="sh-h1" style="font-size:1.5rem">Create your account</div><p class="sh-muted">Start tracking your biological age in under two minutes.</p>')
            with st.form("signup_form"):
                name = st.text_input("Full name", placeholder="Jane Fine")
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                ok = st.form_submit_button("Create account", type="primary", use_container_width=True)
            if ok:
                if not name.strip():
                    st.error("Full name is required.")
                elif not valid_email(email.strip()):
                    st.error("Enter a valid email address.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        uid = repository.create_user(name.strip(), email.strip(), hash_password(password))
                        st.session_state.user = {"id": uid, "name": name.strip(), "email": email.strip().lower()}
                        st.session_state.page = "dashboard"
                        st.rerun()
                    except DatabaseError as exc:
                        st.error(str(exc))
            st.button("Already have an account? Sign in", on_click=navigate, args=("login",), key="to_login")
