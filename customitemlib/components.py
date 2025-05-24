from pydantic import BaseModel

class ItemComponents(BaseModel):
    """
    Current version: 1.21.5
    """
    # https://minecraft.wiki/w/Data_component_format#List_of_components
    # https://misode.github.io/changelog?tags=component
    attribute_modifiers: list[dict] = None
    break_sound: str = None
    damage: int = None
    damage_resistant: dict = None
    enchantable: dict = None
    item_model: str = None
    item_name: str | dict = None
    jukebox_playable: str = None
    lore: str | dict = None
    max_damage: int = None
    max_stack_size: int = None
    profile: dict = None
    rarity: str = None
    repairable: dict = None
    repair_cost: int = None
    tool: dict = None
    unbreakable: dict = None
    weapon: dict = None