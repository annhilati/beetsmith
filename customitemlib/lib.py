import re
import beet
from pydantic import BaseModel
from typing import Type, Generic, TypeVar

class AdditionalFile(BaseModel):
    registry: Type # tag, recipe, etc.
    name: str # namespaced id
    content: dict

# T = TypeVar("T")
def resourceLocation(str: str):
    "Ensures that the argument is formatted like a valid resource location and passes it on"

    if ":" not in str:
        return f"minecraft:{str}"
    
    if not re.match(r"^#?([a-z0-9_\-.]+):([a-z0-9_\-\/\.]+)$", str):
        raise ValueError(f"Invalid ResourceLocation: {str}")
    
    return str