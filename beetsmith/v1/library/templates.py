import re
from typing import Any, Callable, Generic, TypeVar
from dataclasses import dataclass
from beetsmith.library.text_components import TextComponent # Used in modules importing from here <3

InputType = TypeVar("InputType")
RepresentedType = TypeVar("RepresentedType")
#T = TypeVar("T")

def identity(x: InputType, /):
    "Returns the argument"
    return x

@dataclass(unsafe_hash=True)
class Placeholder(Generic[InputType, RepresentedType]):
    """Class representing a placeholder in a template.
    
    ---
    #### Usage
    Use Placeholders in a Template's content, to leave the options for entering a value later without needing to remember the position.
    Specify a function, that will manipulate or validate the value put in later.
    ```
    template = Template({"text": Placeholder("text", Tomato, some_Tomato_to_string_turning_function)})
    ```
    """
    
    name: str
    input_type: InputType
    processor: Callable[[InputType], RepresentedType]

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name
    
    def __str__(self):
        raise Exception("Placeholder should not be used in f-strings")
    
    def resolve(self, input: InputType) -> RepresentedType:
        "Equivalent to `.processor(input)`"
        return self.processor(input)
    
@dataclass
class Template(Generic[RepresentedType]):
    """Class representing a template.
    
    ---
    #### Usage
    Use Templates to define complex nested structures with placeholders, that can be easily filled out.
    Supported nested types are list, dict, Template & Placeholder.
    ```
    template = Template(
        {
            "text": Placeholder("text", str, identity),
            "tags": [
                "tag_number_one",
                "tag_{tag_name}_that_has_a_string_placeholder",
                Placeholder("tags", SomeOminousObject, tuplify)
            ]
        }
    )
    ```
    Generate a normal usable object from the Template by filling out the placeholders:
    ```
    result = template.fullfill(
        {
            "text": "Wow!",
            "tag_name": "Yep, that should be a string!",
            "tags": this_is_some_ominous_object
        }
    )
    ```
    """

    content: RepresentedType

    def fullfill(self, mapping: dict[str: Any]) -> RepresentedType:
        """Retunrs the Template's content with placeholders filled out

        #### Parameters
            - mapping (dict)
                - k: Name of a string placeholder or Placeholder object
                - v: Value to replace the placeholder with (Tuples will get unpacked automatically)

        #### Raises
            - KeyError: If a placeholder key present in the templates content is missing in mapping
        """
        work = self.content
        work = substitute_any_placeholders(work, mapping)
        work = substitute_any_strings(work, mapping)
        return work

def substitute_any_strings(obj: Any, mapping: dict[str, str]) -> Any:
    """Substitutes placeholders in strings in an nested object of any complexity.

    #### Parameters
        - obj: (Any): Currently supported are strings, lists and dicts
        - mapping (dict)
            - k: Name of a placeholder
            - v: Value to replace the placeholder with
    """
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
    """Substitutes Placeholders in an nested object of any complexity.

    #### Parameters
        - obj: (Any): Currently supported are lists, dicts and nested Templates. Placeholders will be replaced, everything else ignored
        - mapping (dict)
            - k: Name of a placeholder
            - v: Value to replace the placeholder with (Tuples will get unpacked automatically)

    #### Raises
        - KeyError: If any key present in a Placeholder isn't given in mapping
    """
    try:

        if isinstance(obj, Placeholder):
            value = obj.resolve(mapping[obj.name])
            if isinstance(value, tuple):
                raise TypeError(f"Cannot insert a tuple outside a list context: {value}")
            return value
    
        elif isinstance(obj, Template):
            return substitute_any_placeholders(obj.fullfill(mapping), mapping)
    
        elif isinstance(obj, list):
            result = []
            for e in obj:
                if isinstance(e, Placeholder):
                    value = e.resolve(mapping[e.name])
                    if isinstance(value, tuple):
                        result.extend(value)
                    else:
                        result.append(value)
                else:
                    result.append(substitute_any_placeholders(e, mapping))
            return result

        elif isinstance(obj, dict):
            return {k: substitute_any_placeholders(v, mapping) for k, v in obj.items()}

        else:
            return obj

    except Exception as e:
        msg = str(e)
        if match := re.search(r"'(\w+)'", msg):
            raise KeyError(f"Template is missing key '{match.group(1)}' for fullfillment")
        raise e