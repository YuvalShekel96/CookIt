# CookIT - Recipe Book Application

A local recipe book app that generates shopping lists, checks supermarket prices, and allows adding items to supermarket carts.

## Features

- 📖 **Recipe Book Management**: Create and manage your recipe collection
- 🛒 **Shopping Lists**: Automatically generate shopping lists from recipes with quantity merging
- 💰 **Price Comparison**: Compare prices across multiple supermarkets
- 💾 **Local Storage**: All data stored locally in JSON format

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the Streamlit UI:

```bash
streamlit run ui/app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Home Page**: View all your dishes, add new dishes, or create shopping lists
2. **Dish Page**: View and edit dish details, ingredients, and cooking steps
3. **Shopping List Page**: View your shopping list, see total costs, and save/load lists
4. **Compare Prices Page**: Compare prices across different supermarkets

### Programmatic Usage

You can also use the CookIT classes programmatically:

```python
from cookit import Book, Dish, Ingredient, ShoppingList, Supermarket
from cookit.storage import save_book, load_book

# Create a recipe book
book = Book("My Recipes")

# Create a dish
pasta = Dish("Spaghetti Carbonara")
pasta.add_ingredient(Ingredient("Pasta", 500.0, "g"))
pasta.add_ingredient(Ingredient("Eggs", 3.0, "pcs"))

# Add dish to book
book.add_dish(pasta)

# Save the book
save_book(book)

# Create a shopping list
shopping_list = ShoppingList()
shopping_list.add_dish(pasta)

# Create a supermarket
supermarket = Supermarket("Store A", delivery_price=5.00)
supermarket.set_price("Pasta", 2.50)
supermarket.set_price("Eggs", 0.50)

# Calculate total cost
total = supermarket.total_cost(shopping_list)
print(f"Total cost: ${total}")
```

## Project Structure

```
CookIT/
├── cookit/              # Core package
│   ├── __init__.py
│   ├── ingredient.py    # Ingredient class
│   ├── dish.py          # Dish class
│   ├── book.py          # Book class
│   ├── shopping_list.py # ShoppingList class
│   ├── supermarket.py   # Supermarket class
│   └── storage.py       # JSON persistence
├── ui/                  # Streamlit UI
│   └── app.py           # Main UI application
├── tests/               # Unit tests
│   ├── test_ingredient.py
│   ├── test_dish.py
│   ├── test_book.py
│   ├── test_shopping_list.py
│   ├── test_supermarket.py
│   └── test_storage.py
├── db/                  # JSON data storage (created automatically)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Running Tests

Run all unit tests:

```bash
python -m pytest tests/
```

Or use unittest:

```bash
python -m unittest discover tests
```

## Data Storage

All data is stored in the `db/` directory as JSON files:
- `book.json` - Recipe book data
- `supermarkets.json` - Supermarket configurations
- `shopping_list_*.json` - Saved shopping lists

## Development

This project follows clean architecture principles:
- Small, focused modules
- Type hints throughout
- Comprehensive docstrings
- Unit tests for all core functionality

## Future Phases

Future enhancements (not yet implemented):
- Supermarket price scraping agents
- API routes
- Server-client architecture
- External API integrations

## License

This project is for local use and development.

