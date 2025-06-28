<img align="right" src="https://github.com/annhilati/beetsmith/blob/main/icon.png" alt="logo" width="74">

# BeetSmith
### Features
- 📚 Item behaviour definition through rigid abstractions
- 📑 YAML-file definition format
- 📂 Automatic implementation of files required for a desired behavior
- ⛓️‍💥 [Beet](https://gitHub.com/mcbeet/beet)-Integration

### Usage
> [!IMPORTANT]
> BeetSmith is still heavily under development, not feature-complete and unstable. 

#### 1. Defining an Item
```py
from customitemlib import CustomItem

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
from customitemlib import CustomItem

def main(ctx: Context):
    item = CustomItem(...)

    item.implement(ctx.data)
```

#### 3. Defining an Item in another way
```yaml
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