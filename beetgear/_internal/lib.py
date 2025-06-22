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

def textComponent(obj: Any) -> list[list[dict]]:
    """Ensures that a text representing object is always a complete and correct formatted multiline text component

    #### Additional use:
        - [0]: if only one line is allowed in the field
    """
    newLines = []

    if type(obj) == list:                       # obj ist Line oder Multiline
        if list in [type(e) for e in obj]:      # obj ist Multiline
            for line in obj:
                if type(line) == str:                   # line ist str
                    newLines.append([{"text": line}])
                elif type(line) == dict:                # line ist dict
                    newLines.append([line])
                elif type(line) == list:                # line ist list
                    newLine = []
                    for part in line:
                        if type(part) == str:               # part ist str
                            newLine.append({"text": part})
                        elif type(part) == dict:            # part ist dict
                            newLine.append(part)
                        else:
                            raise ValueError("Every part in a line in the object has to be a dictionary or a string")
                    newLines.append(newLine)
                else:                                   # line ist nicht str, dict oder list
                    raise ValueError("Every line in the object has to be a list, a dictionary or a string")
        else:                                   # obj ist Line
            newLine = []
            for part in obj:
                if type(part) == str:                   # part ist str
                    newLine.append({"text": part})
                elif type(part) == dict:                # part ist dict
                    newLine.append(part)
            newLines.append(newLine)
    elif type(obj) == dict:
        newLines.append([obj])
    elif type(obj) == str:
        newLines.append([{"text": obj}])
    else:
        ValueError("Object has to be a list, a dictionary or a string")

    return newLines

# def ersetzen_template(obj: Any, mapping: dict[str, Any]) -> Any:
#     if isinstance(obj, str):
#         return string.Template(obj).safe_substitute(mapping)
#     elif isinstance(obj, list):
#         return [ersetzen_template(e, mapping) for e in obj]
#     elif isinstance(obj, dict):
#         return {k: ersetzen_template(v, mapping) for k, v in obj.items()}
#     else:
#         return obj