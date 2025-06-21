import re
import json
import string
from pydantic import BaseModel
from typing import Any, Type, Union, List, Dict

resourceLocationPattern = r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)*$" # currently: never leading special symbols

def resourceLocation(str: str):
    "Ensures that the argument is formatted like a valid resource location and passes it on"

    if ":" not in str:
        str = "minecraft:" + str
    
    if not re.match(resourceLocationPattern, str):
        raise ValueError(f"{str} does not match the pattern of resource loactions")
    
    return str

def textComponent(obj: Any) -> str | dict | list[Any]:
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

def get_structure(obj: Any) -> type:

    if isinstance(obj, str):
        working = str
    elif isinstance(obj, list):
        working = List
        types: set = set()
        if len(obj) == 0:
            working = List[None]
        else:
            for e in obj:
                structure = get_structure(e)
                types.add(structure)
            working = List[Union[tuple(types)]]
    elif isinstance(obj, dict):
        working = Dict
        types: set = set()
        for key, value in obj.items():
            value_structure = get_structure(value)
            if get_structure(key) is not str:
                raise NotImplementedError()
            types.add(value_structure)
        working = Dict[str, Union[tuple(types)]]
    else:
        working = type(obj)

    return working


print(get_structure({"test": ["liste", ["liste"]]}))