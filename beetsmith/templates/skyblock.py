from .core import *

right_click_ability = TextTemplate(
    [
        [{"text": ""}],
        [
            {"color": "gold", "italic": False, "text": "Ability: {ability_name}"},
            {"color": "yellow", "bold": True, "italic": False, "text": " RIGHT CLICK"},
        ],
        Placeholder("description"),
        [
            {"color": "dark_gray", "italic": False, "text": "Cooldown: {cooldown_seconds}s"}
        ]
    ]
)