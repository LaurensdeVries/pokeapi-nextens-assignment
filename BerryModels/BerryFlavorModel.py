from pydantic import BaseModel
from typing import List

class NameUrl(BaseModel):
    name: str
    url: str

class BerryReference(BaseModel):
    potency: int
    berry: NameUrl

class Language(BaseModel):
    name: str
    language: NameUrl

class BerryFlavor(BaseModel):
    """Pydantic model for Berry Flavor data, all fields are required by default"""
    id: int
    name: str
    berries: List[BerryReference]
    contest_type: NameUrl
    names: List[Language]