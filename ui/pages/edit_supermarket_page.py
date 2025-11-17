"""
Edit supermarket page.
"""

import streamlit as st

from cookit.storage import save_supermarkets


def render_edit_supermarket_page() -> None:
    """Page for editing supermarket prices."""
    st.title("⚙️ Edit Supermarket Prices")

    supermarkets = st.session_state.supermarkets
    sm_idx = st.session_state.get("selected_sm_idx", 0)

    if sm_idx >= len(supermarkets):
        st.error("Supermarket not found")
        if st.button("Back"):
            st.session_state.page = "Compare Prices"
        return

    supermarket = supermarkets[sm_idx]
    st.subheader(f"Editing: {supermarket.name}")

    st.markdown("### Current Price Catalog")
    if supermarket.price_catalog:
        for item, price in list(supermarket.price_catalog.items()):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"• {item}")
            with col2:
                st.write(f"${price:.2f}")
            with col3:
                if st.button("Remove", key=f"remove_price_{item}"):
                    del supermarket.price_catalog[item]
                    save_supermarkets(supermarkets)
                    st.rerun()
    else:
        st.info("No prices in catalog yet.")

    st.markdown("---")
    st.markdown("### Add/Edit Price")
    with st.form("add_price_form"):
        item_name = st.text_input("Item Name")
        item_price = st.number_input("Price per Unit", min_value=0.0, value=0.0)

        if st.form_submit_button("Set Price"):
            if item_name:
                supermarket.set_price(item_name, item_price)
                save_supermarkets(supermarkets)
                st.success(f"Set price for {item_name}!")
                st.rerun()

    if st.button("🔙 Back to Compare Prices"):
        st.session_state.page = "Compare Prices"
        st.rerun()

