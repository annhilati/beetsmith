
> [!TIP]
> While being easy to use, this library is not that powerful. There are similar projects like [StewBeet](https://github.com/Stoupy51/StewBeet) and [simple_item_plugin](https://github.com/edayot/simple_item_plugin) that are a lot more powerful. This library mirrors my personal needs for making custom items in Minecraft.

<img align="right" src="https://github.com/annhilati/beetsmith/blob/main/icon.png" alt="logo" height="65">

# BeetSmith
### Features
- 📚 Item behaviour definition through rigid abstractions
- 📑 YAML-file definition format with mild syntax warnings
- 📂 Automatic implementation of files required for a desired behavior
- ⛓️‍💥 [Beet](https://gitHub.com/mcbeet/beet)-Integration

### RoadMap
- [x] [Custom Items](https://github.com/annhilati/beetsmith/issues/38) ~ 70%  
- [ ] Custom Armor Sets ~ 40%

### Usage
> [!IMPORTANT]
> BeetSmith is still heavily under development, not feature-complete and unstable. 

#### 1. Defining an Item
```py
from beetsmith import CustomItem

item = CustomItem(id="custom:test", name="Test", model="nether_star")

item.weapon(attack_damage=10,
            attack_speed=2,
            disable_blocking=5)
item.enchantable(20, "enchantable/sharp_weapon")
item.rarity("uncommon")
```

#### 2. Automatically implementing an Item into a Datapack with beet
```py
# This is a normal beet plugin
from beet import Context
from beetsmith import CustomItem

def main(ctx: Context):
    item = CustomItem(...)

    item.implement(ctx.data)
```

#### 3. Defining an Item in another way
```yaml
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
```py
# another unspectecular beet plugin
from beet import Context
from beetsmith import bulk_implement

def main(ctx: Context):
    bulk_implement("./src/customitems", ctx.data)
```