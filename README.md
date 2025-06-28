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

In a beet plugin `plugin.py` do:
```py
from beet import Context
from customitemlib import CustomItem

def main(ctx: Context):
    item = CustomItem(id="custom:test", name="Test", model="nether_star")

    item.weapon(max_durability=100,
                attack_damage=10,
                attack_speed=2,
                disable_blocking=5,
                break_sound="intentionally_empty")
    item.enchantable(20, "enchantable/sharp_weapon")
    item.rarity("uncommon")

    item.implement(ctx.data)
```
with a `beet.json`:
```json
{
    "data_pack": {
        "load": []
    },
    "pipeline": ["plugin.main"],
    "output": "Example output dir"
}
```
