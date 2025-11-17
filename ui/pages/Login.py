"""
Login and registration page for CookIT.
"""

import sys
from pathlib import Path

import streamlit as st

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from cookit.auth import authenticate, register_user


def _clear_user_state() -> None:
    """Remove user-specific session data."""
    for key in [
        "book",
        "current_shopping_list",
        "page",
        "selected_dish_idx",
        "search_text",
        "selected_labels",
        "temp_ingredients",
    ]:
        if key in st.session_state:
            del st.session_state[key]


def render_login_page(embedded: bool = False) -> None:
    """Render the login/register UI."""
    if not embedded:
        st.set_page_config(page_title="CookIT Login", page_icon="🔐")
        st.title("🔐 CookIT Login")

    if "authenticated_user" in st.session_state:
        st.success(f"Already logged in as {st.session_state['authenticated_user']}.")
        if st.button("🚪 Logout"):
            _clear_user_state()
            st.session_state.pop("authenticated_user", None)
            st.rerun()
        return

    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = authenticate(login_username, login_password)
        if user:
            _clear_user_state()
            st.session_state["authenticated_user"] = user.username
            st.session_state.page = "Home"
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.markdown("---")
    st.subheader("Register")

    register_username = st.text_input("New Username", key="register_username")
    register_password = st.text_input("New Password", type="password", key="register_password")

    if st.button("Create Account"):
        try:
            user = register_user(register_username, register_password)
        except ValueError as exc:
            st.error(str(exc))
        else:
            _clear_user_state()
            st.session_state["authenticated_user"] = user.username
            st.session_state.page = "Home"
            st.success("Account created! You are now logged in.")
            st.rerun()


def main() -> None:
    """Entry point for the Streamlit multipage interface."""
    render_login_page()


if __name__ == "__main__":
    main()

