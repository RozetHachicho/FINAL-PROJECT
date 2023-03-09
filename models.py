from __future__ import annotations

# python built-in imports
from dataclasses import dataclass

# from datetime import datetime


@dataclass
class House:
    id: int
    building_type: str
    house_style: str
    overall_quality: int
    overall_condition: int
    year_built: int
    roof_style: str
    number_full_bathrooms: int
    number_half_bathrooms: int
    number_bedrooms: int
    number_fireplaces: int
    sales_price: int
