from pydantic import BaseModel, HttpUrl

class Language(BaseModel):
    name: str
    url: HttpUrl

class LanguageName(BaseModel):
    name: str
    language: Language

class Berry(BaseModel):
    name: str
    url: HttpUrl

class BerryFirmnessTest(BaseModel):
    """Pydantic model for Berry data, all fields are required by default"""
    id: int
    name: str
    berries: list[Berry]
    names: list[LanguageName]

