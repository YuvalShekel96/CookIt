"""
Add new dish page.
"""

import streamlit as st

from cookit import Dish, Ingredient
from cookit.storage import save_user_book
from ui.constants import MEASUREMENT_OPTIONS
from ui.state import get_current_username


def render_add_dish_page() -> None:
    """Render the add dish form."""
    st.title("➕ Add New Dish")
    username = get_current_username()

    if st.button("🏠 Back to Home"):
        st.session_state.temp_ingredients = []
        st.session_state.ingredient_expander_open = False
        st.session_state.page = "Home"
        st.rerun()

    st.markdown("---")

    if "temp_ingredients" not in st.session_state:
        st.session_state.temp_ingredients = []
    
    # Track if expander should stay open after adding ingredient
    if "ingredient_expander_open" not in st.session_state:
        st.session_state.ingredient_expander_open = False

    if st.session_state.temp_ingredients:
        st.subheader("Current Ingredients")
        for i, ing in enumerate(st.session_state.temp_ingredients):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"• {ing.name}")
            with col2:
                st.write("")
            with col3:
                if st.button("Remove", key=f"remove_temp_ing_{i}"):
                    st.session_state.temp_ingredients.pop(i)
                    st.rerun()

    with st.expander("➕ Add Ingredient", expanded=st.session_state.ingredient_expander_open):
        with st.form("add_ingredient_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                ing_name = st.text_input("Name", key="new_ing_name")
            with col2:
                ing_quantity = st.number_input("Quantity", min_value=0, key="new_ing_qty")
            with col3:
                ing_unit = st.selectbox(
                    "Unit",
                    options=MEASUREMENT_OPTIONS,
                    key="new_ing_unit_add_dish",
                )

            if st.form_submit_button("Add Ingredient"):
                if ing_name:
                    new_ingredient = Ingredient(ing_name, ing_quantity, ing_unit)
                    st.session_state.temp_ingredients.append(new_ingredient)
                    st.session_state.ingredient_expander_open = True  # Keep expander open
                    st.rerun()
                else:
                    st.warning("Please enter a name for the ingredient")

    st.markdown("---")

    with st.form("add_dish_form"):
        name = st.text_input("Dish Name *", placeholder="e.g., Spaghetti Carbonara")
        labels = st.text_input("Labels (comma-separated)", placeholder="e.g., vegetarian, quick")

        st.markdown("### Cooking Steps")
        steps_text = st.text_area("Steps (one per line)")

        submitted = st.form_submit_button("Create Dish")

        if submitted:
            if not name:
                st.error("Dish name is required!")
            else:
                labels_list = [l.strip() for l in labels.split(",") if l.strip()]
                steps_list = [s.strip() for s in steps_text.split("\n") if s.strip()]

                new_dish = Dish(
                    name=name,
                    ingredients=st.session_state.temp_ingredients.copy(),
                    labels=labels_list,
                    steps=steps_list,
                )

                st.session_state.book.add_dish(new_dish)
                save_user_book(username, st.session_state.book)
                st.success(f"Dish '{name}' created!")
                st.session_state.temp_ingredients = []
                st.session_state.ingredient_expander_open = False
                st.session_state.page = "Home"
                st.rerun()

