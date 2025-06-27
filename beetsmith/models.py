from pydantic import BaseModel
from typing import Type

class ItemComponents(BaseModel):
    # https://minecraft.wiki/w/Data_component_format#List_of_components
    # https://misode.github.io/changelog?tags=component
    attribute_modifiers: list[dict] = None
    block_attacks: dict = None
    break_sound: str = None
    consumable: dict = None
    custom_data: dict = None
    damage: int = None
    damage_resistant: dict = None
    death_protection: dict = None
    dyed_color: int | list = None
    enchantable: dict = None
    enchantment_glint_override: bool = None
    equippable: dict = None
    food: dict = None
    glider: dict = None
    instrument: dict = None
    item_model: str = None
    item_name: str | dict | list = None
    jukebox_playable: str = None
    lore: str | dict | list = None
    max_damage: int = None
    max_stack_size: int = None
    profile: dict = None
    potion_content: dict = None
    rarity: str = None
    repairable: dict = None
    repair_cost: int = None
    tool: dict = None
    trim: dict = None
    unbreakable: dict = None
    use_cooldown: dict = None
    use_remainder: dict = None
    weapon: dict = None

class RegistryFile(BaseModel):
    registry: Type # tag, recipe, etc.
    name: str # namespaced id
    content: dict | list[str]

    def __str__(self):
        return f"<{self.registry.__name__} '{self.name}'>"
    
# class YAMLItemDefinition(BaseModel):
#     id: str
#     name: str
#     model: str
#     texture: str = None
#     damagable: dict = None
#     enchantable: dict = None
#     environment_resistance: dict = None
#     lore: str | dict | list = None
#     rarity: dict = None
#     right_click_ability: dict = None
#     attribute_modifier: dict = None
#     weapon: dict = None