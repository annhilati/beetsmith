from pydantic import BaseModel
from typing import Type

class AdditionalFile(BaseModel):
    type: Type # tag, recipe, etc.
    name: str # namespaced id
    content: dict

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