"""
Settings page for user preferences.
"""

import streamlit as st

from cookit.auth import save_user
from ui.state import get_current_user


def render_settings_page() -> None:
    """Allow the user to update delivery address and enabled supermarkets."""
    user = get_current_user()
    st.title("⚙️ Account Settings")
    st.caption(f"Signed in as **{user.username}**")

    existing_supermarkets = st.session_state.get("supermarkets", [])
    available_supermarket_names = sorted({sm.name for sm in existing_supermarkets})

    current_enabled = user.enabled_supermarkets or []
    default_multiselect = [name for name in current_enabled if name in available_supermarket_names]
    custom_names = [name for name in current_enabled if name not in available_supermarket_names]
    custom_default = ", ".join(custom_names)

    with st.form("settings_form"):
        delivery_address = st.text_area(
            "Delivery Address",
            value=user.delivery_address,
            placeholder="Street, City, Zip, etc.",
        )

        selected_existing = st.multiselect(
            "Enabled Supermarkets (from configured list)",
            options=available_supermarket_names,
            default=default_multiselect,
            help="Only supermarkets configured in the Compare Prices page appear here.",
        )

        custom_supermarkets = st.text_input(
            "Custom Supermarkets (comma-separated)",
            value=custom_default,
            placeholder="e.g., Local Mart, Organic Shop",
            help="Use this if you shop at stores not listed above.",
        )

        submitted = st.form_submit_button("Save Settings")

        if submitted:
            custom_list = [name.strip() for name in custom_supermarkets.split(",") if name.strip()]
            updated_list = sorted(set(selected_existing + custom_list))
            user.delivery_address = delivery_address.strip()
            user.enabled_supermarkets = updated_list
            save_user(user)
            st.success("Settings saved!")

    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

