import re
import json
import string
from pydantic import BaseModel
from typing import Any, Type

resourceLocationPattern = r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)*$" # currently: never leading special symbols

def resourceLocation(str: str):
    "Ensures that the argument is formatted like a valid resource location and passes it on"

    if ":" not in str:
        str = "minecraft:" + str
    
    if not re.match(resourceLocationPattern, str):
        raise ValueError(f"{str} does not match the pattern of resource loactions")
    
    return str

def textComponent(obj: str | dict | list[Any]) -> str | dict | list[Any]:
    if isinstance(obj, str):
        try:
            work = json.loads(obj)
        except Exception as e:
            work = obj
    else:
        work = obj
    
    return work

def ersetzen_template(obj: Any, mapping: dict[str, Any]) -> Any:
    if isinstance(obj, str):
        return string.Template(obj).safe_substitute(mapping)
    elif isinstance(obj, list):
        return [ersetzen_template(e, mapping) for e in obj]
    elif isinstance(obj, dict):
        return {k: ersetzen_template(v, mapping) for k, v in obj.items()}
    else:
        return obj
