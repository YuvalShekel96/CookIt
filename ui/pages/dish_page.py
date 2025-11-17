"""
Dish details page.
"""

import streamlit as st

from cookit import Ingredient
from cookit.storage import save_user_book, save_user_shopping_list
from ui.constants import MEASUREMENT_OPTIONS
from ui.state import get_current_username


def render_dish_page() -> None:
    """Display a single dish with editing controls."""
    st.title("📝 Dish Details")

    top_col1, top_col2 = st.columns(2)
    book = st.session_state.book
    dish_idx = st.session_state.get("selected_dish_idx", 0)
    username = get_current_username()

    if dish_idx >= len(book.dishes):
        st.error("Dish not found")
        with top_col2:
            if st.button("🏠 Back to Home", key="back_to_home_top_missing"):
                st.session_state.page = "Home"
                st.rerun()
        return

    dish = book.dishes[dish_idx]

    with top_col1:
        if st.button("🏠 Back to Home", key="back_to_home_top"):
            st.session_state.page = "Home"
            st.rerun()
    with top_col2:
        if st.button("🛒 Add to Shopping List", key="add_to_shopping_list_top"):
            st.session_state.current_shopping_list.add_dish(dish)
            save_user_shopping_list(username, st.session_state.current_shopping_list)
            st.success(f"Added {dish.name} to shopping list!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        new_name = st.text_input("Dish Name", value=dish.name, key="dish_name")
        new_labels = st.text_input(
            "Labels (comma-separated)",
            value=", ".join(dish.labels),
            key="dish_labels",
        )

    with col2:
        if st.button("💾 Save Changes"):
            dish.name = new_name
            dish.labels = [l.strip() for l in new_labels.split(",") if l.strip()]
            save_user_book(username, book)
            st.success("Dish saved!")

        if st.button("🗑️ Delete Dish"):
            book.remove_dish(dish)
            save_user_book(username, book)
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")
    st.subheader("Ingredients")

    for i, ingredient in enumerate(dish.ingredients):
        col1, col2, col3= st.columns([3, 1, 1])
        with col1:
            st.write(f"• {ingredient.name}")
        with col2:
            if ingredient.price_per_unit:
                st.write(f"${ingredient.price_per_unit:.2f}/{ingredient.unit_type}")
            else:
                st.write("No price")
        with col3:
            if st.button("Remove", key=f"remove_ing_{i}"):
                dish.remove_ingredient(ingredient)
                save_user_book(username, book)
                st.rerun()

    with st.expander("➕ Add Ingredient"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ing_name = st.text_input("Name", key="new_ing_name")
        with col2:
            ing_quantity = st.number_input("Quantity", min_value=0, key="new_ing_qty")
        with col3:
            ing_unit = st.selectbox(
                "Unit",
                options=MEASUREMENT_OPTIONS,
                key="new_ing_unit_select",
            )

        if st.button("Add Ingredient"):
            if ing_name:
                new_ingredient = Ingredient(ing_name, ing_quantity, ing_unit)
                dish.add_ingredient(new_ingredient)
                save_user_book(username, book)
                st.rerun()

    st.markdown("---")
    st.subheader("Cooking Steps")

    for i, step in enumerate(dish.steps):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.write(f"{i + 1}. {step}")
        with col2:
            if st.button("🗑️", key=f"remove_step_{i}"):
                dish.steps.pop(i)
                save_user_book(username, book)
                st.rerun()

    new_step = st.text_area("Add Step", key="new_step")
    if st.button("Add Step"):
        if new_step.strip():
            dish.steps.append(new_step.strip())
            save_user_book(username, book)
            st.rerun()

    st.markdown("---")

