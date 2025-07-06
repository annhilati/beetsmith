import string
from typing import Any, Type, Callable, Generic, TypeVar
from ..text_components import TextComponent # Used in modules importing from here <3

T = TypeVar("T")

def identity(x):
    "Returns the argument"
    return x

class Placeholder(Generic[T]):
    "BeetSmith object placeholder"
    
    def __init__(self, name: str, input_type: T, validator: Callable):
        self.name = name
        self.input_type = input_type
        self.validator = validator

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name
    
    def __str__(self):
        raise Exception("Can't use Placeholder in strings")
    
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
        work = format_any(work, {key: value for key, value in mapping.items()})
        work = replace_placeholders(work, {key: value for key, value in mapping.items()})
        return work

def format_any(obj: Any, mapping: dict[str, str]) -> Any:
    "Replaces string placeholders in objects of any complexity"
    if isinstance(obj, str):
        return string.Template(obj).safe_substitute(mapping)
    
    elif isinstance(obj, list):
        return [format_any(e, mapping) for e in obj]
    
    elif isinstance(obj, dict):
        return {k: format_any(v, mapping) for k, v in obj.items()}
    
    else:
        return obj

def replace_placeholders(obj: Any, mapping: dict[str, Any]) -> Any:
    """Replace Placeholder objects in obj of any complexity

    #### Parameters:
        - obj: (Any): Currently supported are lists and dicts. Placeholders will be replaced, everything else ignored
        - mapping (dict)
            - k: Name of a placeholder
            - v: Value to replace the placeholder with (Tuples will get unpacked automatically)
    """
    
    if isinstance(obj, list):
        result = []
        for e in obj:
            replaced = replace_placeholders(e, mapping)
            if isinstance(e, Placeholder) and isinstance(replaced, tuple):
                result.extend(replaced)
            else:
                result.append(replaced)
        return result

    elif isinstance(obj, dict):
        return {k: replace_placeholders(v, mapping) for k, v in obj.items()}

    elif isinstance(obj, Placeholder):
        return obj.validator(mapping[obj.name])

    else:
        return obj