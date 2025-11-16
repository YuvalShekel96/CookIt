"""
ShoppingList module for CookIT.

Represents a shopping list that can merge ingredients from multiple dishes.
"""

from typing import List
from cookit.ingredient import Ingredient
from cookit.dish import Dish


class ShoppingList:
    """
    Represents a shopping list with merged ingredients.
    
    When adding dishes, ingredients with the same name and unit_type
    are automatically merged by summing their quantities.
    
    Attributes:
        items: List of merged ingredients
    """
    
    def __init__(self, items: List[Ingredient] = None):
        """
        Initialize a ShoppingList.
        
        Args:
            items: Optional initial list of ingredients
        """
        self.items = items if items is not None else []
    
    def add_item(self, ingredient: Ingredient) -> None:
        """
        Add an ingredient to the shopping list.
        
        If an ingredient with the same name and unit_type already exists,
        the quantities are merged (summed).
        
        Args:
            ingredient: Ingredient to add or merge
        """
        # Check if ingredient already exists (same name and unit_type)
        for existing_item in self.items:
            if existing_item == ingredient:
                # Merge quantities
                existing_item.units_required += ingredient.units_required
                # Update price if the new ingredient has price info
                if ingredient.price_per_unit is not None:
                    existing_item.price_per_unit = ingredient.price_per_unit
                    existing_item.source_supermarket = ingredient.source_supermarket
                return
        
        # If not found, add as new item
        # Create a copy to avoid modifying the original
        new_ingredient = Ingredient(
            name=ingredient.name,
            units_required=ingredient.units_required,
            unit_type=ingredient.unit_type,
            price_per_unit=ingredient.price_per_unit,
            source_supermarket=ingredient.source_supermarket,
        )
        self.items.append(new_ingredient)
    
    def add_dish(self, dish: Dish) -> None:
        """
        Add all ingredients from a dish to the shopping list.
        
        Ingredients are automatically merged if they already exist.
        
        Args:
            dish: Dish to add ingredients from
        """
        for ingredient in dish.ingredients:
            self.add_item(ingredient)
    
    def remove_dish(self, dish: Dish) -> bool:
        """
        Remove all ingredients from a dish from the shopping list.
        
        Note: This subtracts quantities. If quantity becomes zero or negative,
        the item is removed entirely.
        
        Args:
            dish: Dish to remove ingredients from
            
        Returns:
            True if any ingredients were removed/modified, False otherwise
        """
        modified = False
        ingredients_to_remove = []
        
        for dish_ingredient in dish.ingredients:
            for shopping_item in self.items:
                if shopping_item == dish_ingredient:
                    shopping_item.units_required -= dish_ingredient.units_required
                    modified = True
                    # Remove if quantity is zero or negative
                    if shopping_item.units_required <= 0:
                        ingredients_to_remove.append(shopping_item)
                    break
        
        # Remove items with zero or negative quantities
        for item in ingredients_to_remove:
            self.items.remove(item)
        
        return modified
    
    def total_cost(self):
        """
        Calculate the total cost of all items in the shopping list.

        Returns:
            The total cost (float) if all items have prices, or None if any item is missing a price.
        """
        total = 0.0
        for item in self.items:
            item_price = item.total_price()
            if item_price is None:
                return None
            total += item_price
        return total
    def __repr__(self) -> str:
        """String representation of the shopping list."""
        return f"ShoppingList({len(self.items)} items)"
    
    def to_dict(self) -> dict:
        """
        Convert shopping list to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the shopping list
        """
        return {
            "items": [item.to_dict() for item in self.items],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ShoppingList":
        """
        Create a ShoppingList from a dictionary.
        
        Args:
            data: Dictionary containing shopping list data
            
        Returns:
            ShoppingList instance
        """
        items = [
            Ingredient.from_dict(item_data) for item_data in data.get("items", [])
        ]
        return cls(items=items)

