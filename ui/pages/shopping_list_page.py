"""
Shopping list page.
"""

import streamlit as st
from cookit import Ingredient
from cookit.storage import (
    list_shopping_lists,
    load_shopping_list,
    save_shopping_list,
    save_user_shopping_list,
)
from ui.constants import MEASUREMENT_OPTIONS
from ui.state import get_current_username


def render_shopping_list_page() -> None:
    """Display the shopping list page."""
    st.title("🛒 Shopping List")
    username = get_current_username()
    st.markdown("---")
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    st.markdown("---")
    shopping_list = st.session_state.current_shopping_list
    
    # Initialize shopping_list_dishes if not exists
    if "shopping_list_dishes" not in st.session_state:
        st.session_state.shopping_list_dishes = []
    
    # Track if add item expander should stay open
    if "add_item_expander_open" not in st.session_state:
        st.session_state.add_item_expander_open = False

    # Display dishes section
    if st.session_state.shopping_list_dishes:
        st.subheader("Dishes in Shopping List")
        dish_cols = st.columns(3)
        for idx, dish in enumerate(st.session_state.shopping_list_dishes):
            col = dish_cols[idx % 3]
            with col:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"🍽️ **{dish.name}**")
                with col2:
                    if st.button("Remove Dish", key=f"remove_dish_{idx}"):
                        shopping_list.remove_dish(dish)
                        st.session_state.shopping_list_dishes.remove(dish)
                        save_user_shopping_list(username, shopping_list)
                        st.rerun()
        st.markdown("---")

    # Add item form
    with st.expander("➕ Add Item", expanded=st.session_state.add_item_expander_open):
        with st.form("add_item_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                item_name = st.text_input("Name", key="new_item_name")
            with col2:
                item_quantity = st.number_input("Quantity", min_value=0, value=0, key="new_item_qty")
            with col3:
                item_unit = st.selectbox(
                    "Unit",
                    options=MEASUREMENT_OPTIONS,
                    key="new_item_unit",
                )
            
            if st.form_submit_button("Add Item"):
                if item_name:
                    new_ingredient = Ingredient(item_name, item_quantity, item_unit)
                    shopping_list.add_item(new_ingredient)
                    st.session_state.add_item_expander_open = True
                    save_user_shopping_list(username, shopping_list)
                    st.rerun()
                else:
                    st.warning("Please enter a name for the item")
    
    st.markdown("---")

    if not shopping_list.items:
        st.info("Your shopping list is empty. Add dishes from the home page!")
    else:
        st.subheader("Items")
        total_cost = shopping_list.total_cost()

        for i, item in enumerate(shopping_list.items):
            col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
            with col1:
                st.write(f"• **{item.name}**")
            with col2:
                # Editable quantity
                new_qty = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=int(item.units_required),
                    key=f"qty_{i}",
                    label_visibility="collapsed"
                )
                if new_qty != item.units_required:
                    item.units_required = new_qty
                    save_user_shopping_list(username, shopping_list)
                    st.rerun()
            with col3:
                st.write(f"{item.unit_type}")
            with col4:
                if item.price_per_unit:
                    st.write(f"${item.price_per_unit:.2f}/{item.unit_type}")
                else:
                    st.write("No price")
            with col5:
                item_total = item.total_price()
                if item_total:
                    st.write(f"**${item_total:.2f}**")
                else:
                    st.write("—")
            with col6:
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
                        # Reset dishes list when loading (dishes info not stored in saved lists)
                        st.session_state.shopping_list_dishes = []
                        save_user_shopping_list(username, loaded)
                        st.success(f"Loaded '{selected_list}'!")
                        st.rerun()


