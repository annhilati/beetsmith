import re
import beet
from pydantic import BaseModel
from typing import Type, Generic, TypeVar

class AdditionalFile(BaseModel):
    type: Type # tag, recipe, etc.
    name: str # namespaced id
    content: dict

T = TypeVar("T")
class ResourceLocation(Generic[T]):
    "Represents a resource location, more commonly known as a namespaced id like `minecraft:diamond`"
    def __init__(self, value: str):
        """
        Represents a resource location, more commonly known as a namespaced id like `minecraft:diamond`

        #### Usage:
        Only pass as a
        """
        if isinstance(value, ResourceLocation):
            value = str(value)

        if ":" not in value:
            value = f"minecraft:{value}"
        
        if not re.match(r"^[a-z0-9_\-.]+:[a-z0-9_\-\/\.]+$", value):
            raise ValueError(f"Invalid ResourceLocation: {value}")
        
        self.namespace, self.path = value.split(":", 1)

    def __str__(self):
        return f"{self.namespace}:{self.path}"
    
    def __repr__(self):
        return f"ResourceLocation('{self}')"
    
    def __eq__(self, other):
        if isinstance(other, ResourceLocation):
            return (self.namespace, self.path) == (other.namespace, other.path)
        return False

class SoundEvent: ...
class Item: ...

def ensureResourceLocation(str: str) -> str:
    for char in str.lower():
        if char not in "abcdefghijklmnopqrstuvwxyz_/:":
            raise ValueError(f"{str} is not a valid resource location")
        
    if str.startswith(":") or str.endswith(":"):
        raise ValueError(f"{str} is not a valid resource location")
    
    if str.count(":") == 1:
        return str
    elif str.count(":") == 0:
        return f"minecraft:{str}"
    else:
        raise ValueError(f"{str} is not a valid resource location")

