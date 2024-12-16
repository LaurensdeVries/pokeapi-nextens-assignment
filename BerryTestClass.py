from pydantic import BaseModel
from typing import List

class NameUrlBase(BaseModel):
    name: str
    url: str

class Flavor(BaseModel):
    potency: int
    flavor: NameUrlBase

class Berry(BaseModel):
    """Pydantic model for Berry data, all fields are required by default"""
    id: int
    name: str
    growth_time: int
    max_harvest: int
    natural_gift_power: int
    size: int
    smoothness: int
    soil_dryness: int
    firmness: NameUrlBase
    flavors: List[Flavor]
    item: NameUrlBase
    natural_gift_type: NameUrlBase
