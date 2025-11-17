"""
Shopping list page.
"""

import streamlit as st

from cookit.storage import (
    list_shopping_lists,
    load_shopping_list,
    save_shopping_list,
    save_user_shopping_list,
)
from ui.state import get_current_username


def render_shopping_list_page() -> None:
    """Display the shopping list page."""
    st.title("🛒 Shopping List")
    username = get_current_username()

    shopping_list = st.session_state.current_shopping_list

    if not shopping_list.items:
        st.info("Your shopping list is empty. Add dishes from the home page!")
    else:
        st.subheader("Items")
        total_cost = shopping_list.total_cost()

        for i, item in enumerate(shopping_list.items):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.write(f"• **{item.name}**")
            with col2:
                st.write(f"{item.units_required} {item.unit_type}")
            with col3:
                if item.price_per_unit:
                    st.write(f"${item.price_per_unit:.2f}/{item.unit_type}")
                else:
                    st.write("No price")
            with col4:
                item_total = item.total_price()
                if item_total:
                    st.write(f"**${item_total:.2f}**")
                else:
                    st.write("—")
            with col5:
                if st.button("Remove", key=f"remove_item_{i}"):
                    shopping_list.items.pop(i)
                    save_user_shopping_list(username, shopping_list)
                    st.rerun()

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if total_cost:
                st.metric("Total Estimated Cost", f"${total_cost:.2f}")
            else:
                st.info("Some items are missing prices. Total cost cannot be calculated.")

        with col2:
            if st.button("💰 Compare Prices"):
                st.session_state.page = "Compare Prices"
                st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        list_name = st.text_input("Save as", placeholder="e.g., Weekly Shopping")
        if st.button("💾 Save List"):
            if list_name:
                save_shopping_list(shopping_list, list_name, username)
                st.success(f"Shopping list saved as '{list_name}'!")
            else:
                st.error("Please enter a name for the shopping list")

    with col2:
        saved_lists = list_shopping_lists(username)
        if saved_lists:
            selected_list = st.selectbox("Load Shopping List", [""] + saved_lists)
            if st.button("📂 Load List"):
                if selected_list:
                    loaded = load_shopping_list(selected_list, username)
                    if loaded:
                        st.session_state.current_shopping_list = loaded
                        save_user_shopping_list(username, loaded)
                        st.success(f"Loaded '{selected_list}'!")
                        st.rerun()

    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

