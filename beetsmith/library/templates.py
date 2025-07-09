import re
from typing import Any, Callable, Generic, TypeVar
from beetsmith.library.text_components import TextComponent # Used in modules importing from here <3

T = TypeVar("T")

def identity(x):
    "Returns the argument"
    return x

class Placeholder(Generic[T]):
    "BeetSmith object placeholder"
    
    def __init__(self, name: str, input_type: T, validator: Callable[[T], Any] = identity):
        self.name = name
        self.input_type = input_type
        self.validator = validator

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name
    
    def __str__(self):
        raise Exception("Placeholder should not be used in f-strings")
    
class Template(Generic[T]):
    "BeetSmith template for complex objects"
    def __init__(self, value: T):
        self.content = value

    def fullfill(self, mapping: dict[str: Any]) -> Any:
        """Replace the Template's placeholders

        #### Parameters:
            - mapping (dict)
                - k: Name of a string placeholder or Placeholder object
                - v: Value to replace the placeholder with (Tuples will get unpacked automatically)
        """
        work = self.content
        work = substitute_any_strings(work, mapping)
        work = substitute_any_placeholders(work, mapping)
        return work

def substitute_any_strings(obj: Any, mapping: dict[str, str]) -> Any:
    "Replaces string placeholders in objects of any complexity"
    try:
    
        if isinstance(obj, str):
            return obj.format(**mapping)
        
        elif isinstance(obj, list):
            return [substitute_any_strings(e, mapping) for e in obj]
        
        elif isinstance(obj, dict):
            return {k: substitute_any_strings(v, mapping) for k, v in obj.items()}
        
        else:
            return obj
        
    except Exception as e:
        msg = str(e)
        if match := re.search(r"'(\w+)'", msg):
            raise KeyError(f"Template is missing key '{match.group(1)}' for fullfillment")
        raise e

def substitute_any_placeholders(obj: Any, mapping: dict[str, Any]) -> Any:
    """Replace Placeholder objects in obj of any complexity

    #### Parameters:
        - obj: (Any): Currently supported are lists and dicts. Placeholders will be replaced, everything else ignored
        - mapping (dict)
            - k: Name of a placeholder
            - v: Value to replace the placeholder with (Tuples will get unpacked automatically)
    """
    try:
        if isinstance(obj, list):
            result = []
            for e in obj:
                if isinstance(e, Placeholder):
                    value = e.validator(mapping[e.name])
                    if isinstance(value, tuple):
                        result.extend(value)
                    else:
                        result.append(value)
                else:
                    result.append(substitute_any_placeholders(e, mapping))
            return result

        elif isinstance(obj, dict):
            return {k: substitute_any_placeholders(v, mapping) for k, v in obj.items()}

        elif isinstance(obj, Placeholder):
            value = obj.validator(mapping[obj.name])
            if isinstance(value, tuple):
                raise TypeError(f"Cannot insert a tuple outside a list context: {value}")
            return value
    
        else:
            return obj

    except Exception as e:
        msg = str(e)
        if match := re.search(r"'(\w+)'", msg):
            raise KeyError(f"Template is missing key '{match.group(1)}' for fullfillment")
        raise e