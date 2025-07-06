"""
## Typewriter
BeetSmith sub-library for crafting, manipulating and formatting object templates
"""

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Exports                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

from .templates import Placeholder, Template
from .skyblock import right_click_ability

_symbols = [Placeholder, Template]
_constants = "right_click_ability"

__all__ = [obj.__name__ for obj in _symbols].extend(_constants)