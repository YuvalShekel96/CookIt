"""
Dish module for CookIT.

Represents a recipe dish with ingredients, steps, and metadata.
"""

from typing import Optional, List
from cookit.ingredient import Ingredient


class Dish:
    """
    Represents a recipe dish.
    
    Attributes:
        name: Name of the dish
        ingredients: List of ingredients required
        type: Optional dish type (e.g., "Main Course", "Dessert")
        labels: List of labels/tags (e.g., ["vegetarian", "quick"])
        steps: List of cooking steps
    """
    
    def __init__(
        self,
        name: str,
        ingredients: Optional[List[Ingredient]] = None,
        dish_type: Optional[str] = None,
        labels: Optional[List[str]] = None,
        steps: Optional[List[str]] = None,
    ):
        """
        Initialize a Dish.
        
        Args:
            name: Name of the dish
            ingredients: Optional list of ingredients
            dish_type: Optional dish type
            labels: Optional list of labels
            steps: Optional list of cooking steps
        """
        self.name = name
        self.ingredients = ingredients if ingredients is not None else []
        self.type = dish_type
        self.labels = labels if labels is not None else []
        self.steps = steps if steps is not None else []
    
    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        Add an ingredient to the dish.
        
        Args:
            ingredient: Ingredient to add
        """
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, ingredient: Ingredient) -> bool:
        """
        Remove an ingredient from the dish.
        
        Args:
            ingredient: Ingredient to remove
            
        Returns:
            True if ingredient was found and removed, False otherwise
        """
        try:
            self.ingredients.remove(ingredient)
            return True
        except ValueError:
            return False
    
    def __repr__(self) -> str:
        """String representation of the dish."""
        return f"Dish({self.name}, {len(self.ingredients)} ingredients)"
    
    def to_dict(self) -> dict:
        """
        Convert dish to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the dish
        """
        return {
            "name": self.name,
            "ingredients": [ing.to_dict() for ing in self.ingredients],
            "type": self.type,
            "labels": self.labels,
            "steps": self.steps,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Dish":
        """
        Create a Dish from a dictionary.
        
        Args:
            data: Dictionary containing dish data
            
        Returns:
            Dish instance
        """
        ingredients = [
            Ingredient.from_dict(ing_data) for ing_data in data.get("ingredients", [])
        ]
        return cls(
            name=data["name"],
            ingredients=ingredients,
            dish_type=data.get("type"),
            labels=data.get("labels", []),
            steps=data.get("steps", []),
        )

