# CookIT - Recipe Book Application

A local recipe book app that generates shopping lists, checks supermarket prices, and allows adding items to supermarket carts.

## Features

- 📖 **Recipe Book Management**: Create and manage your recipe collection
- 🛒 **Shopping Lists**: Automatically generate shopping lists from recipes with quantity merging
- 💰 **Price Comparison**: Compare prices across multiple supermarkets
- 💾 **Per-User Local Storage**: Each user has isolated books and shopping lists
- 🔐 **Local Authentication**: Username/password login with hashed credentials

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

1. **Login Page**: Register a username and password or log in to an existing account
2. **Home Page**: View all your dishes, add new dishes, or create shopping lists
3. **Dish Page**: View and edit dish details, ingredients, and cooking steps
4. **Shopping List Page**: View your shopping list, see total costs, and save/load lists
5. **Compare Prices Page**: Compare prices across different supermarkets
6. **Settings Page**: Update delivery address and preferred supermarkets per user

### Programmatic Usage

You can also use the CookIT classes programmatically:

```python
from cookit import Dish, Ingredient, Supermarket
from cookit.storage import save_user_book, load_user_book, load_user_shopping_list

# Use a username to scope data
username = "demo_user"

# Load or create a recipe book for this user
book = load_user_book(username)

# Create a dish
pasta = Dish("Spaghetti Carbonara")
pasta.add_ingredient(Ingredient("Pasta", 500.0, "g"))
pasta.add_ingredient(Ingredient("Eggs", 3.0, "pcs"))

# Add dish to book
book.add_dish(pasta)

# Save the book for this user
save_user_book(username, book)

# Create a shopping list
shopping_list = load_user_shopping_list(username)
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
│   ├── enums.py         # Shared enums
│   ├── auth.py          # Local authentication helpers
│   └── storage.py       # JSON persistence
├── ui/                  # Streamlit UI
│   ├── app.py           # Main UI application
│   └── pages/
│       └── Login.py     # Login/Register page
├── tests/               # Unit tests
│   ├── test_ingredient.py
│   ├── test_dish.py
│   ├── test_book.py
│   ├── test_shopping_list.py
│   ├── test_supermarket.py
│   ├── test_storage.py
│   └── test_auth.py
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

## Authentication & Data Storage

- User accounts live in `db/users.json` (passwords stored as SHA256 hashes).
- Each user’s data is isolated under `db/users/<username>_*.json`.
  - `*_book.json` – recipe book
  - `*_shopping_list.json` – current shopping list
  - `*_shopping_list_<name>.json` – saved lists
- Global data such as supermarkets remains under `db/`.

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

