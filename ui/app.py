"""
Streamlit UI for CookIT.

Provides a local web interface for managing recipes, shopping lists, and price comparisons.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path to import cookit
sys.path.insert(0, str(Path(__file__).parent.parent))

from cookit import Book, Dish, Ingredient, ShoppingList, Supermarket
from cookit.enums import MeasurementUnit
from cookit.storage import (
    save_book,
    load_book,
    save_supermarkets,
    load_supermarkets,
    save_shopping_list,
    load_shopping_list,
    list_shopping_lists,
)


# Page configuration
st.set_page_config(
    page_title="CookIT - Recipe Book",
    page_icon="🍳",
    layout="wide",
)

MEASUREMENT_OPTIONS = MeasurementUnit.choices()


def initialize_session_state():
    """Initialize session state variables."""
    if "book" not in st.session_state:
        book = load_book()
        if book is None:
            book = Book("My Recipe Book")
            save_book(book)
        st.session_state.book = book
    
    if "supermarkets" not in st.session_state:
        supermarkets = load_supermarkets()
        st.session_state.supermarkets = supermarkets
    
    if "current_shopping_list" not in st.session_state:
        st.session_state.current_shopping_list = ShoppingList()
    
    if "page" not in st.session_state:
        st.session_state.page = "Home"


def home_page():
    """Display the home page with list of dishes."""
    st.title("🍳 CookIT - Recipe Book")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add Dish", use_container_width=True):
            st.session_state.page = "Add Dish"
    with col2:
        if st.button("🛒 Create Shopping List", use_container_width=True):
            st.session_state.page = "Shopping List"
    with col3:
        if st.button("💰 Compare Prices", use_container_width=True):
            st.session_state.page = "Compare Prices"
    
    st.markdown("---")

    book = st.session_state.book
    
    
    if not book.dishes:
        st.info("No dishes in your recipe book yet. Click 'Add Dish' to get started!")
    else:
        st.subheader("Your Dishes")
        # INSERT_YOUR_CODE

        # Filter/search section
        filter_col1, filter_col2 = st.columns([2, 2])

        with filter_col1:
            search_text = st.text_input("🔎 Search by name", value=st.session_state.get("search_text", ""), key="search_text")
        with filter_col2:
            all_labels = book.get_all_labels() if hasattr(book, "get_all_labels") else []
            selected_labels = st.multiselect(
                "🏷️ Filter by labels", 
                options=sorted(all_labels), 
                default=st.session_state.get("selected_labels", []),
                key="selected_labels"
            )

        filtered_dishes = book.dishes

        # If label filters
        if selected_labels:
            filtered_dishes = book.get_dish_by_label(selected_labels)

        # If search box; search within filtered_by_label dishes
        if search_text:
            # Only retain those matching the search in the filtered list
            # book.get_dish_by_name_regex returns all dishes matching regex, so intersect with already label-filtered
            name_matches = set(book.get_dish_by_name_regex(search_text))
            filtered_dishes = [dish for dish in filtered_dishes if dish in name_matches]

        # Always show dishes sorted by name (display only)
        sorted_dishes = sorted(filtered_dishes, key=lambda d: d.name.lower())
        # Display dishes in columns
        cols = st.columns(3)
        for idx, dish in enumerate(sorted_dishes):
            col = cols[idx % 3]
            with col:
                with st.container():
                    st.markdown(f"### {dish.name}")
                    if dish.type:
                        st.caption(f"Type: {dish.type}")
                    if dish.labels:
                        st.caption(f"Labels: {', '.join(dish.labels)}")
                    st.caption(f"{len(dish.ingredients)} ingredients")
                    
                    # idx here is display index; we map to real index for action-based buttons
                    real_idx = book.dishes.index(dish)
                    
                    if st.button("Open Dish", key=f"open_{idx}"):
                        st.session_state.page = "Dish"
                        st.session_state.selected_dish_idx = real_idx
                    
                    if st.button("Add to Shopping List", key=f"add_to_list_{idx}"):
                        st.session_state.current_shopping_list.add_dish(dish)
                        st.success(f"Added {dish.name} to shopping list!")


def dish_page():
    """Display a dish page with editable fields."""
    st.title("📝 Dish Details")

    # Place the buttons at the very top of the page using st.columns, right after the title
    top_col1, top_col2 = st.columns(2)
    book = st.session_state.book
    dish_idx = st.session_state.get("selected_dish_idx", 0)

    # If not found, don't reference dish
    if dish_idx >= len(book.dishes):
        st.error("Dish not found")
        with top_col2:
            if st.button("🏠 Back to Home", key="back_to_home_top"):
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
            st.success(f"Added {dish.name} to shopping list!")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Editable fields
    col1, col2 = st.columns(2)

    with col1:
        new_name = st.text_input("Dish Name", value=dish.name, key="dish_name")
        new_type = st.text_input("Type", value=dish.type or "", key="dish_type")
        new_labels = st.text_input(
            "Labels (comma-separated)",
            value=", ".join(dish.labels),
            key="dish_labels",
        )

    with col2:
        if st.button("💾 Save Changes"):
            dish.name = new_name
            dish.type = new_type if new_type else None
            dish.labels = [l.strip() for l in new_labels.split(",") if l.strip()]
            save_book(book)
            st.success("Dish saved!")

        if st.button("🗑️ Delete Dish"):
            book.remove_dish(dish)
            save_book(book)
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # Ingredients section
    st.subheader("Ingredients")

    for i, ingredient in enumerate(dish.ingredients):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"• {ingredient.name}")
        with col2:
            st.write(f"{ingredient.units_required} {ingredient.unit_type}")
        with col3:
            if ingredient.price_per_unit:
                st.write(f"${ingredient.price_per_unit:.2f}/{ingredient.unit_type}")
            else:
                st.write("No price")
        with col4:
            if st.button("Remove", key=f"remove_ing_{i}"):
                dish.remove_ingredient(ingredient)
                save_book(book)
                st.rerun()

    # Add ingredient form
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
                save_book(book)
                st.rerun()

    # Steps section
    st.markdown("---")
    st.subheader("Cooking Steps")

    for i, step in enumerate(dish.steps):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.write(f"{i + 1}. {step}")
        with col2:
            if st.button("🗑️", key=f"remove_step_{i}"):
                dish.steps.pop(i)
                save_book(book)
                st.rerun()

    # Add step form
    new_step = st.text_area("Add Step", key="new_step")
    if st.button("Add Step"):
        if new_step.strip():
            dish.steps.append(new_step.strip())
            save_book(book)
            st.rerun()

    st.markdown("---")


def add_dish_page():
    """Page for adding a new dish."""
    st.title("➕ Add New Dish")
    
    # Initialize ingredients list in session state if not exists
    if "temp_ingredients" not in st.session_state:
        st.session_state.temp_ingredients = []
    
    # Display current ingredients
    if st.session_state.temp_ingredients:
        st.subheader("Current Ingredients")
        for i, ing in enumerate(st.session_state.temp_ingredients):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"• {ing.name}")
            with col2:
                st.write(f"{ing.units_required} {ing.unit_type}")
            with col3:
                st.write("")
            with col4:
                if st.button("Remove", key=f"remove_temp_ing_{i}"):
                    st.session_state.temp_ingredients.pop(i)
                    st.rerun()
    
    # Add ingredient section (outside form)
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
                key="new_ing_unit_add_dish",
            )
        
        if st.button("Add Ingredient"):
            if ing_name:
                new_ingredient = Ingredient(ing_name, ing_quantity, ing_unit)
                st.session_state.temp_ingredients.append(new_ingredient)
                st.rerun()
            else:
                st.warning("Please enter a name for the ingredient")
    
    st.markdown("---")
    
    # Form for dish details
    with st.form("add_dish_form"):
        name = st.text_input("Dish Name *", placeholder="e.g., Spaghetti Carbonara")
        dish_type = st.text_input("Type", placeholder="e.g., Main Course")
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
                    ingredients=st.session_state.temp_ingredients.copy(),  # Use session state ingredients
                    dish_type=dish_type if dish_type else None,
                    labels=labels_list,
                    steps=steps_list,
                )
                
                st.session_state.book.add_dish(new_dish)
                save_book(st.session_state.book)
                st.success(f"Dish '{name}' created!")
                # Clear temporary ingredients
                st.session_state.temp_ingredients = []
                st.session_state.page = "Home"
                st.rerun()
    
    if st.button("🏠 Back to Home"):
        # Clear temporary ingredients when going back
        if "temp_ingredients" in st.session_state:
            st.session_state.temp_ingredients = []
        st.session_state.page = "Home"
        st.rerun()


def shopping_list_page():
    """Display the shopping list page."""
    st.title("🛒 Shopping List")
    
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
    
    # Save shopping list
    col1, col2 = st.columns(2)
    with col1:
        list_name = st.text_input("Save as", placeholder="e.g., Weekly Shopping")
        if st.button("💾 Save List"):
            if list_name:
                save_shopping_list(shopping_list, list_name)
                st.success(f"Shopping list saved as '{list_name}'!")
            else:
                st.error("Please enter a name for the shopping list")
    
    with col2:
        # Load shopping list
        saved_lists = list_shopping_lists()
        if saved_lists:
            selected_list = st.selectbox("Load Shopping List", [""] + saved_lists)
            if st.button("📂 Load List"):
                if selected_list:
                    loaded = load_shopping_list(selected_list)
                    if loaded:
                        st.session_state.current_shopping_list = loaded
                        st.success(f"Loaded '{selected_list}'!")
                        st.rerun()
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "Home"
        st.rerun()


def compare_prices_page():
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
    
    # Display comparison table
    st.subheader("Price Comparison")
    
    comparison_data = []
    for supermarket in supermarkets:
        total = supermarket.total_cost(shopping_list)
        comparison_data.append({
            "Supermarket": supermarket.name,
            "Items Cost": total - supermarket.delivery_price if total else None,
            "Delivery": supermarket.delivery_price,
            "Total": total,
        })
    
    st.dataframe(comparison_data, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed breakdown per supermarket
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
    
    # Manage supermarkets
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


def edit_supermarket_page():
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
    
    # Display current catalog
    st.markdown("### Current Price Catalog")
    if supermarket.price_catalog:
        for item, price in supermarket.price_catalog.items():
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
    
    # Add/Edit price
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


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == "Home":
        home_page()
    elif page == "Dish":
        dish_page()
    elif page == "Add Dish":
        add_dish_page()
    elif page == "Shopping List":
        shopping_list_page()
    elif page == "Compare Prices":
        compare_prices_page()
    elif page == "Edit Supermarket":
        edit_supermarket_page()
    else:
        st.session_state.page = "Home"
        st.rerun()


if __name__ == "__main__":
    main()

