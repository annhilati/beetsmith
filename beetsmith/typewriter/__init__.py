"""
## Typewriter
BeetSmith sub-library for crafting, manipulating and formatting text components
"""

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Exports                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

from .core import Placeholder, TextTemplate
from .skyblock import right_click_ability

def _export(*objs):
    return [obj.__name__ for obj in objs]

__all__ = _export(Placeholder, TextTemplate)