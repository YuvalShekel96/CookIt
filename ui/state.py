"""
Session state helpers for the CookIT Streamlit UI.
"""

import streamlit as st

from cookit.auth import get_user


def get_current_username() -> str:
    """Return the username stored in session state."""
    username = st.session_state.get("authenticated_user")
    if not username:
        raise RuntimeError("User is not authenticated.")
    return username


def get_current_user():
    """Return the current authenticated User object."""
    username = get_current_username()
    user = get_user(username)
    if user is None:
        raise RuntimeError("Authenticated user record could not be found.")
    return user


def logout_user() -> None:
    """Clear user-specific session state and rerun app."""
    for key in [
        "authenticated_user",
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
    st.rerun()

