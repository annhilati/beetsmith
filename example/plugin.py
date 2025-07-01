from beet import Context
from beetsmith import bulk_implement, CustomItem, create_from_yaml, create_from_yaml

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

    item = create_from_yaml("./src/beetsmith/customitem/aspect_of_the_dragons.yaml")
    item.implement(ctx.data)