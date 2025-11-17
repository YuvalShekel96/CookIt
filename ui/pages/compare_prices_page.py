"""
Compare prices page.
"""

import streamlit as st

from cookit import Supermarket
from cookit.storage import save_supermarkets


def render_compare_prices_page() -> None:
    """Display price comparison across supermarkets."""
    st.title("💰 Compare Prices")

    shopping_list = st.session_state.current_shopping_list
    supermarkets = st.session_state.supermarkets

    if not shopping_list.items:
        st.warning("Your shopping list is empty. Add items first!")
        if st.button("🏠 Back to Home"):
            st.session_state.page = "Home"
        return

    if not supermarkets:
        st.info("No supermarkets configured. Add supermarkets to compare prices.")
        if st.button("🏠 Back to Home"):
            st.session_state.page = "Home"
        return

    st.subheader("Price Comparison")

    comparison_data = []
    for supermarket in supermarkets:
        total = supermarket.total_cost(shopping_list)
        comparison_data.append(
            {
                "Supermarket": supermarket.name,
                "Items Cost": total - supermarket.delivery_price if total else None,
                "Delivery": supermarket.delivery_price,
                "Total": total,
            }
        )

    st.dataframe(comparison_data, use_container_width=True)
    st.markdown("---")

    for supermarket in supermarkets:
        with st.expander(f"📊 {supermarket.name} - Detailed Breakdown"):
            total = supermarket.total_cost(shopping_list)

            if total is None:
                st.warning("Some items are missing prices in this supermarket's catalog.")
            else:
                st.write(f"**Delivery Fee:** ${supermarket.delivery_price:.2f}")
                st.write(f"**Total Cost:** ${total:.2f}")
                st.markdown("### Itemized Prices")
                for item in shopping_list.items:
                    price = supermarket.get_price(item.name)
                    if price:
                        item_cost = price * item.units_required
                        st.write(
                            f"• {item.name}: {item.units_required} {item.unit_type} × "
                            f"${price:.2f}/{item.unit_type} = ${item_cost:.2f}"
                        )
                    else:
                        st.write(f"• {item.name}: Price not available")

            if supermarket.website_url:
                st.markdown(f"[🔗 Open {supermarket.name} Website]({supermarket.website_url})")

    st.markdown("---")

    with st.expander("⚙️ Manage Supermarkets"):
        st.subheader("Add Supermarket")
        with st.form("add_supermarket_form"):
            sm_name = st.text_input("Supermarket Name")
            sm_delivery = st.number_input("Delivery Price", min_value=0.0, value=0.0)
            sm_url = st.text_input("Website URL")

            if st.form_submit_button("Add Supermarket"):
                if sm_name:
                    new_sm = Supermarket(sm_name, sm_delivery, sm_url)
                    supermarkets.append(new_sm)
                    save_supermarkets(supermarkets)
                    st.success(f"Added {sm_name}!")
                    st.rerun()

        st.markdown("---")
        st.subheader("Existing Supermarkets")
        for i, sm in enumerate(supermarkets):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{sm.name}**")
                st.caption(f"Delivery: ${sm.delivery_price:.2f}")
            with col2:
                if st.button("Edit Prices", key=f"edit_prices_{i}"):
                    st.session_state.page = "Edit Supermarket"
                    st.session_state.selected_sm_idx = i
                    st.rerun()
            with col3:
                if st.button("Delete", key=f"delete_sm_{i}"):
                    supermarkets.pop(i)
                    save_supermarkets(supermarkets)
                    st.rerun()

    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

