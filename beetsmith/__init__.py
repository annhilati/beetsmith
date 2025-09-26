"""
## BeetSmith
A python library for defining custom Minecraft items through rigid abstractions.

The library provides methods for defining an item's behaviour and makes use of Minecraft's item components for implementation.

BeetSmith can be used standalone for generating JSON or can be used with beet for implementing custom items in the course of beet's pipeline.

---

#### 1. Defining an Item
```
from beetsmith import CustomItem

item = CustomItem(id="custom:test", name="Test", model="nether_star")

item.weapon(attack_damage=10,
            attack_speed=2,
            disable_blocking=5)
item.enchantable(20, "enchantable/sharp_weapon")
item.rarity("uncommon")
```

#### 2. Automatically implementing an Item into a Datapack with beet
```
# This is a normal beet plugin
from beet import Context
from beetsmith import CustomItem

def main(ctx: Context):
    item = CustomItem(...)

    item.implement(ctx.data)
```

#### 3. Defining an Item in another way
```
# this is ./src/customitems/testitem.yml
type: CustomItem
name: Test
model: nether_star
behaviour:
    - weapon:
        attack_damage: 10
        attack_speed: 2
        disable_blocking: 5
    - enchantable:
        enchantability: 20
        enchantable_tag: enchantable/sharp_weapon
    - rarity:
        rarity: uncommon
```
... and loading a lot of such files with beet ...
```
# another unspectecular beet plugin
from beet import Context
from beetsmith import bulk_implement

def main(ctx: Context):
    bulk_implement("./src/customitems", ctx.data)
```
"""

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Exports                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

import beet
from beetsmith.v2.library.components import (ItemComponents, REMOVED)
from beetsmith.v2.core.resourcelocations import (ResourceLocationChecker)
from beetsmith.v2.library.item import (Item)

_symbols = [Item,
            ItemComponents,
            beet]
_constants = ["REMOVED"]

__all__ = [obj.__name__ for obj in _symbols].extend(_constants)

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Config                                    │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

import warnings as _warnings
def warning(message, category, filename, lineno, file=None, line=None):
    print(f"{filename}\n  BeetSmith: {message}")

_warnings.showwarning = warning