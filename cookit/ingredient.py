"""
Ingredient module for CookIT.

Represents a single ingredient with quantity, unit, and optional pricing information.
"""

from typing import Optional


class Ingredient:
    """
    Represents a single ingredient in a recipe.
    
    Attributes:
        name: The name of the ingredient (e.g., "Tomatoes")
        units_required: The quantity needed (e.g., 500.0)
        unit_type: The unit of measurement (e.g., "g", "ml", "pcs", "pack")
        price_per_unit: Optional price per unit from a supermarket
        source_supermarket: Optional name of the supermarket providing the price
    """
    
    def __init__(
        self,
        name: str,
        units_required: float,
        unit_type: str,
        price_per_unit: Optional[float] = None,
        source_supermarket: Optional[str] = None,
    ):
        """
        Initialize an Ingredient.
        
        Args:
            name: Name of the ingredient
            units_required: Quantity needed
            unit_type: Unit of measurement
            price_per_unit: Optional price per unit
            source_supermarket: Optional supermarket name
        """
        self.name = name
        self.units_required = units_required
        self.unit_type = unit_type
        self.price_per_unit = price_per_unit
        self.source_supermarket = source_supermarket
    
    def total_price(self) -> Optional[float]:
        """
        Calculate the total price for this ingredient.
        
        Returns:
            Total price (units_required * price_per_unit) if price_per_unit is set,
            None otherwise.
        """
        if self.price_per_unit is None:
            return None
        return self.units_required * self.price_per_unit
    
    def __repr__(self) -> str:
        """String representation of the ingredient."""
        price_str = f" @ ${self.price_per_unit}/{self.unit_type}" if self.price_per_unit else ""
        return f"Ingredient({self.name}, {self.units_required} {self.unit_type}{price_str})"
    
    def __eq__(self, other: object) -> bool:
        """Check equality based on name, units, and unit_type."""
        if not isinstance(other, Ingredient):
            return False
        return (
            self.name.lower() == other.name.lower()
            and self.unit_type == other.unit_type
        )
    
    def to_dict(self) -> dict:
        """
        Convert ingredient to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the ingredient
        """
        return {
            "name": self.name,
            "units_required": self.units_required,
            "unit_type": self.unit_type,
            "price_per_unit": self.price_per_unit,
            "source_supermarket": self.source_supermarket,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ingredient":
        """
        Create an Ingredient from a dictionary.
        
        Args:
            data: Dictionary containing ingredient data
            
        Returns:
            Ingredient instance
        """
        return cls(
            name=data["name"],
            units_required=data["units_required"],
            unit_type=data["unit_type"],
            price_per_unit=data.get("price_per_unit"),
            source_supermarket=data.get("source_supermarket"),
        )

