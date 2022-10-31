from lib2to3.pytree import Base
from typing import Optional
from unicodedata import name
from pydantic import BaseModel

class Item(BaseModel):
    name        : str
    quantity    : int
    image_url   : Optional[str]