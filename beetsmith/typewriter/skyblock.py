import textwrap
from .templates import *

def description(text: str) -> tuple[list[dict]]:
    "Converts a text into a line-wrapped tuple of gray colored text lines"
    wrapped = textwrap.wrap(text, width=40)
    print(wrapped)
    print([[line] for line in wrapped])
    normalized = TextComponent.normalize([[line] for line in wrapped])
    for line in normalized:
        for segment in line:
            segment["color"] = "gray"
    return (normalized,)

right_click_ability: Template[list[list[dict]]] = Template(
    [
        [{"text": ""}],
        [
            {"text": "Ability: {ability_name} ", "color": "gold", "italic": False},
            {"text": "RIGHT CLICK", "color": "yellow", "bold": True, "italic": False},
        ],
        Placeholder("description", str, description),
        [
            {"text": "Cooldown: {cooldown_seconds}s", "color": "dark_gray", "italic": False}
        ]
    ]
)
"""
#### Placeholders
    - ability_name (str)
    - cooldown_seconds (str)
    - description (str)
"""