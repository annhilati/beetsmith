import re
from typing import Any

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
        else:                                   # obj ist line mit parts
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

def armor_durability(*, helmet: int = None, chestplate: int = None, leggings: int = None, boots: int = None):
    
    if len([arg for arg in [helmet, chestplate, leggings, boots] if type(arg) != None]) in [0, 2, 3]:
        raise ValueError("Please state one durability")
    
    # obere Liste ist der zu berechnende Slot, untere Liste der bekannte Slot
    factors = [
        [1, 0.6875, 0.7333, 0.8412],
        [1.4546, 1, 1.0667, 1.2284],
        [1.3637, 0.9375, 1, 1.1505],
        [1.1887, 0.8152, 0.8690, 1]
    ]

    durabilities = [helmet, chestplate, leggings, boots]

    for slot, durability in enumerate(durabilities):
        if durability is None:
            for other_slot, other_durability in enumerate(durabilities):
                if other_durability is not None:
                    durabilities[slot] = round(durabilities[other_slot] * factors[slot][other_slot])
    
    return durabilities

def refer(function: function, /):
    """
    Calls another function with the arguments passed into the decorated function
    #### Usage
    ```
    @refer(lib.this_function)
    def new_function():
        ...
    ```
    """
    if isinstance(function, classmethod) or isinstance(function, staticmethod):
        function = function.__func__

    def decorator(method):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator