"""
Book module for CookIT.

Represents a recipe book containing multiple dishes.
"""

from typing import List, Optional
from cookit.dish import Dish
from cookit.ingredient import Ingredient


class Book:
    """
    Represents a recipe book containing multiple dishes.
    
    Attributes:
        name: Name of the recipe book
        dishes: List of dishes in the book
    """
    
    def __init__(self, name: str, dishes: Optional[List[Dish]] = None):
        """
        Initialize a Book.
        
        Args:
            name: Name of the recipe book
            dishes: Optional list of dishes
        """
        self.name = name
        self.dishes = dishes if dishes is not None else []
    
    def add_dish(self, dish: Dish) -> None:
        """
        Add a dish to the book.
        
        Args:
            dish: Dish to add
        """
        self.dishes.append(dish)
    
    def remove_dish(self, dish: Dish) -> bool:
        """
        Remove a dish from the book.
        
        Args:
            dish: Dish to remove
            
        Returns:
            True if dish was found and removed, False otherwise
        """
        try:
            self.dishes.remove(dish)
            return True
        except ValueError:
            return False
    
    def find_dish(self, name: str) -> Optional[Dish]:
        """
        Find a dish by name (case-insensitive).
        
        Args:
            name: Name of the dish to find
            
        Returns:
            Dish if found, None otherwise
        """
        name_lower = name.lower()
        for dish in self.dishes:
            if dish.name.lower() == name_lower:
                return dish
        return None
    
    def get_all_ingredients(self) -> List[Ingredient]:
        """
        Get all unique ingredients from all dishes in the book.
        
        Note: This returns all ingredients without merging duplicates.
        For merged quantities, use ShoppingList.add_dish() instead.
        
        Returns:
            List of all ingredients from all dishes
        """
        all_ingredients = []
        for dish in self.dishes:
            all_ingredients.extend(dish.ingredients)
        return all_ingredients
    
    def __repr__(self) -> str:
        """String representation of the book."""
        return f"Book({self.name}, {len(self.dishes)} dishes)"
    
    def to_dict(self) -> dict:
        """
        Convert book to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the book
        """
        return {
            "name": self.name,
            "dishes": [dish.to_dict() for dish in self.dishes],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Create a Book from a dictionary.
        
        Args:
            data: Dictionary containing book data
            
        Returns:
            Book instance
        """
        dishes = [Dish.from_dict(dish_data) for dish_data in data.get("dishes", [])]
        return cls(name=data["name"], dishes=dishes)

