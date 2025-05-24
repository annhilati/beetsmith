"""
## CustomItemLib
A python library for defining strong abstracted custom Minecraft items that can be implemented via Datapacks.

The library provides methods for setting an item's properties and then makes use of Minecraft's item components for implementation.

CustomItemLib can be used standalone for generating JSON or can be used with beet to implement items in beet's pipeline.

---

### Defining an item
```
from customitemlib import CustomItem

item = CustomItem("Test", "minecraft:diamond")
item.weapon(max_durability=100,
            attack_damage=10,
            attack_speed=2,
            disable_blocking=5,
            break_sound="intentionally_empty")
item.enchantable(20, "enchantable/sharp_weapon")
item.rarity("uncommon")
```

---
### Implementing an item automatically with beet
In a beet plugin:
```
from beet import Context
from customitemlib import CustomItem

def main(ctx: Context):
    item = CustomItem(id="custom:test", name="Test", model="nether_star")

    item.implement(ctx.data)
```
"""

from .customitem import *

__all__ = ["Material"]