from beet import Context
from customitemlib import CustomItem

def main(ctx: Context):
    item = CustomItem(id="custom:test", name="Test", model="minecraft:diamond")
    item.weapon(attack_damage=10,
                attack_speed=2,
                can_sweep=True,
                disable_blocking=5)
    item.enchantable(20, "enchantable/sharp_weapon")
    item.rarity("uncommon")
    item.environment_resistance(True, True)
    item.right_click_ability(description="", cooldown=8, function="this_function:does_not_exist")

    item.implement(ctx.data)