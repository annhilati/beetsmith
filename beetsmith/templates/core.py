import string
from typing import Any

class Placeholder():
    "BeetSmith object placeholder"
    
    def __init__(self, name: str):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Any):
        return self.name == other.name
    
class TextTemplate():
    "BeetSmith template for complex text components"
    def __init__(self, value: list[list[dict]]):
        self.content = value

    def fullfill(self, mapping: dict[str | Placeholder: str | Any]) -> list[list[dict]]:
        work = self.content
        work = replace_string_placeholders(work, {key: value for key, value in mapping if isinstance(key, str)})
        work = replace_placeholders(work, {key: value for key, value in mapping if isinstance(key, Placeholder)})
        return work


def replace_string_placeholders(obj: Any, mapping: dict[str, str]) -> Any:
    "Replaces string placeholders in objects of any complexity"
    if isinstance(obj, str):
        return string.Template(obj).safe_substitute(mapping)
    elif isinstance(obj, list):
        return [replace_string_placeholders(e, mapping) for e in obj]
    elif isinstance(obj, dict):
        return {k: replace_string_placeholders(v, mapping) for k, v in obj.items()}
    else:
        return obj

def replace_placeholders(obj: Any, mapping: dict[Placeholder, Any]) -> Any:
    if isinstance(obj, str):
        return obj
    
    elif isinstance(obj, list):
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
        return mapping[obj]

    else:
        return obj