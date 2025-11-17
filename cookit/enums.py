"""
Enum definitions for the CookIT application.
"""

from enum import Enum
from typing import List


class MeasurementUnit(str, Enum):
    """Enumeration of supported measurement units for ingredients."""

    KG = "kg"
    G = "gram"
    PCS = "pcs"
    LTR = "ltr"
    ML = "ml"

    @classmethod
    def choices(cls) -> List[str]:
        """Return all enum values as a list for UI selections."""
        return [unit.value for unit in cls]

