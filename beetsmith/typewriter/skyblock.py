import textwrap
from ..text_components import TextComponent
from .core import *

def description(text: str):
    wrapped = textwrap.wrap(text, width=40)
    print(wrapped)
    print([[line] for line in wrapped])
    normalized = TextComponent.normalize([[line] for line in wrapped])
    for line in normalized:
        for segment in line:
            segment["color"] = "gray"
    return normalized

right_click_ability = TextTemplate(
    [
        [{"text": ""}],
        [
            {"color": "gold", "italic": False, "text": "Ability: {ability_name}"},
            {"color": "yellow", "bold": True, "italic": False, "text": " RIGHT CLICK"},
        ],
        Placeholder("description", str, description),
        [
            {"color": "dark_gray", "italic": False, "text": "Cooldown: {cooldown_seconds}s"}
        ]
    ]
)
"""
#### Placeholders
    - ability_name (str)
    - cooldown_seconds (str)
    - description (str)
"""