from beet import Context
from beetsmith import bulk_implement, CustomItem, load_from_yaml, load_from_yaml, typewriter, beetsmither

def main(ctx: Context):
    # item = CustomItem(id="custom:test", name="Test", model="minecraft:diamond")
    # item.weapon(attack_damage=10,
    #             attack_speed=2,
    #             can_sweep=True,
    #             disable_blocking=5)
    # item.enchantable(20, "enchantable/sharp_weapon")
    # item.rarity("uncommon")
    # item.environment_resistance(True, True)
    # item.right_click_ability(description="", cooldown=8, function="this_function:does_not_exist")

    #bulk_implement("./src/beetsmith/customitem", ctx.data, allow_raises=False)

    print(ctx.directory)

    ctx.require(beetsmither())