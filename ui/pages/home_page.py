"""
Home page rendering for CookIT.
"""

import streamlit as st

from cookit.storage import save_user_shopping_list
from ui.state import get_current_username, logout_user


def render_home_page() -> None:
    """Display the home page with dish list and navigation."""
    st.title("🍳 CookIT - Recipe Book")
    st.markdown("---")
    username = get_current_username()

    info_col, logout_col = st.columns([3, 1])
    with info_col:
        st.caption(f"Logged in as **{username}**")
    with logout_col:
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Dish", use_container_width=True):
            st.session_state.page = "Add Dish"
    with col2:
        if st.button("🛒 Create Shopping List", use_container_width=True):
            st.session_state.page = "Shopping List"
    with col3:
        if st.button("💰 Compare Prices", use_container_width=True):
            st.session_state.page = "Compare Prices"
    with col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "Settings"

    st.markdown("---")

    book = st.session_state.book

    if not book.dishes:
        st.info("No dishes in your recipe book yet. Click 'Add Dish' to get started!")
        return

    st.subheader("Your Dishes")

    filter_col1, filter_col2 = st.columns([2, 2])

    with filter_col1:
        search_text = st.text_input(
            "🔎 Search by name",
            value=st.session_state.get("search_text", ""),
            key="search_text",
        )
    with filter_col2:
        all_labels = book.get_all_labels() if hasattr(book, "get_all_labels") else []
        selected_labels = st.multiselect(
            "🏷️ Filter by labels",
            options=sorted(all_labels),
            default=st.session_state.get("selected_labels", []),
            key="selected_labels",
        )

    filtered_dishes = book.dishes

    if selected_labels and hasattr(book, "get_dish_by_label"):
        filtered_dishes = book.get_dish_by_label(selected_labels)

    if search_text and hasattr(book, "get_dish_by_name_regex"):
        name_matches = set(book.get_dish_by_name_regex(search_text))
        filtered_dishes = [dish for dish in filtered_dishes if dish in name_matches]

    sorted_dishes = sorted(filtered_dishes, key=lambda d: d.name.lower())
    cols = st.columns(3)
    for idx, dish in enumerate(sorted_dishes):
        col = cols[idx % 3]
        with col:
            with st.container():
                st.markdown(f"### {dish.name}")
                if dish.labels:
                    st.caption(f"Labels: {', '.join(dish.labels)}")
                st.caption(f"{len(dish.ingredients)} ingredients")

                real_idx = st.session_state.book.dishes.index(dish)

                if st.button("Open Dish", key=f"open_{idx}"):
                    st.session_state.page = "Dish"
                    st.session_state.selected_dish_idx = real_idx

                if st.button("Add to Shopping List", key=f"add_to_list_{idx}"):
                    st.session_state.current_shopping_list.add_dish(dish)
                    st.success(f"Added {dish.name} to shopping list!")
                    save_user_shopping_list(username, st.session_state.current_shopping_list)

