from beet import DataPack, Context, LootTable
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