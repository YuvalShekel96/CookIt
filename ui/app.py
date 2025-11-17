"""
Streamlit UI for CookIT.

Provides a local web interface for managing recipes, shopping lists, and price comparisons.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import cookit
sys.path.insert(0, str(Path(__file__).parent.parent))

from cookit.storage import load_supermarkets, load_user_book, load_user_shopping_list
from pages.Login import render_login_page
from pages.add_dish_page import render_add_dish_page
from pages.compare_prices_page import render_compare_prices_page
from pages.dish_page import render_dish_page
from pages.edit_supermarket_page import render_edit_supermarket_page
from pages.home_page import render_home_page
from pages.settings_page import render_settings_page
from pages.shopping_list_page import render_shopping_list_page
from ui.state import get_current_username


# Page configuration
st.set_page_config(
    page_title="CookIT - Recipe Book",
    page_icon="🍳",
    layout="wide",
)

def require_authentication() -> None:
    """Block access unless the user is authenticated."""
    if "authenticated_user" in st.session_state:
        return
    render_login_page(embedded=True)
    st.stop()


def initialize_session_state() -> None:
    """Initialize session state variables for the authenticated user."""
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if "authenticated_user" not in st.session_state:
        return

    username = get_current_username()

    if "book" not in st.session_state:
        st.session_state.book = load_user_book(username)

    if "supermarkets" not in st.session_state:
        st.session_state.supermarkets = load_supermarkets()

    if "current_shopping_list" not in st.session_state:
        st.session_state.current_shopping_list = load_user_shopping_list(username)


def main():
    """Main application entry point."""
    require_authentication()
    initialize_session_state()
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == "Home":
        render_home_page()
    elif page == "Dish":
        render_dish_page()
    elif page == "Add Dish":
        render_add_dish_page()
    elif page == "Shopping List":
        render_shopping_list_page()
    elif page == "Settings":
        render_settings_page()
    elif page == "Compare Prices":
        render_compare_prices_page()
    elif page == "Edit Supermarket":
        render_edit_supermarket_page()
    else:
        st.session_state.page = "Home"
        st.rerun()


if __name__ == "__main__":
    main()

