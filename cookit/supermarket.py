"""
Supermarket module for CookIT.

Represents a supermarket with pricing information and delivery costs.
"""

from typing import Optional, Dict
from cookit.shopping_list import ShoppingList


class Supermarket:
    """
    Represents a supermarket with pricing catalog and delivery information.
    
    Attributes:
        name: Name of the supermarket
        delivery_price: Delivery fee
        website_url: URL of the supermarket website
        price_catalog: Dictionary mapping item names to prices per unit
    """
    
    def __init__(
        self,
        name: str,
        delivery_price: float = 0.0,
        website_url: str = "",
        price_catalog: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize a Supermarket.
        
        Args:
            name: Name of the supermarket
            delivery_price: Delivery fee
            website_url: Website URL
            price_catalog: Optional dictionary of item prices
        """
        self.name = name
        self.delivery_price = delivery_price
        self.website_url = website_url
        self.price_catalog = price_catalog if price_catalog is not None else {}
    
    def set_price(self, item: str, price: float) -> None:
        """
        Set the price for an item in the catalog.
        
        Args:
            item: Name of the item
            price: Price per unit
        """
        self.price_catalog[item] = price
    
    def get_price(self, item: str) -> Optional[float]:
        """
        Get the price for an item from the catalog.
        
        Args:
            item: Name of the item
            
        Returns:
            Price if found, None otherwise
        """
        return self.price_catalog.get(item)
    
    def total_cost(self, shopping_list: ShoppingList) -> Optional[float]:
        """
        Calculate the total cost of a shopping list at this supermarket.
        
        This includes item prices and delivery fee.
        Returns None if any item in the shopping list doesn't have a price
        in the catalog.
        
        Args:
            shopping_list: Shopping list to calculate cost for
            
        Returns:
            Total cost (items + delivery) if all items have prices, None otherwise
        """
        total = 0.0
        
        for item in shopping_list.items:
            # Try to get price from catalog
            price = self.get_price(item.name)
            if price is None:
                # If item doesn't have price in catalog, return None
                return None
            
            # Calculate cost for this item
            item_cost = price * item.units_required
            total += item_cost
        
        # Add delivery price
        total += self.delivery_price
        
        return total
    
    def __repr__(self) -> str:
        """String representation of the supermarket."""
        return f"Supermarket({self.name}, {len(self.price_catalog)} items in catalog)"
    
    def to_dict(self) -> dict:
        """
        Convert supermarket to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the supermarket
        """
        return {
            "name": self.name,
            "delivery_price": self.delivery_price,
            "website_url": self.website_url,
            "price_catalog": self.price_catalog,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Supermarket":
        """
        Create a Supermarket from a dictionary.
        
        Args:
            data: Dictionary containing supermarket data
            
        Returns:
            Supermarket instance
        """
        return cls(
            name=data["name"],
            delivery_price=data.get("delivery_price", 0.0),
            website_url=data.get("website_url", ""),
            price_catalog=data.get("price_catalog", {}),
        )

