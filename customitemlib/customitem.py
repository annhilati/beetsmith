# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#
# https://minecraft.wiki/w/Data_component_format#List_of_components
# TODO: Armor, Armorsets, Food, Abilities

import json
from pydantic import BaseModel

class ItemComponents(BaseModel):
    """
    Current version: 1.21.5
    """
    attribute_modifier: list[dict] = None
    break_sound: str = None
    damage: int = None
    enchantable: dict = None
    item_model: str = None
    item_name: str | dict = None
    jukebox_playable: str = None
    max_damage: int = None
    max_stack_size: int = None
    profile: dict = None
    rarity: str = None
    repairable: dict = None
    tool: dict = None
    unbreakable: dict = None
    weapon: dict = None

class CustomItem():
    "Data model representing a custom item"
    def __init__(self, name: str | dict, model: str):
        """
        Data model representing a custom item

        #### Parameters
            - name (str | dict): Name of the item as a plain string or text component as a dict
            - model (str): Asset name of the items model

        #### Modifier
            Can be set by asigning a value to these properties
            - damagable
            - enchantable
            - headtexture (str): The items texture if it has a player head model as encoded base64
            - rarity
            - weapon
        """

        self._item = "minecraft:music_disc_11"
        self.removed_components = ["jukebox_playable"]
        self.components = ItemComponents()
        self.components.item_name = name
        self.components.item_model = model
        self.components.max_stack_size = 64

    @property
    def rarity(self):
        if self.components.rarity:
            return self.components.rarity
        return "common"
    
    @rarity.setter
    def rarity(self, rarity: str):
        self.components.rarity = rarity
    
    @property
    def headtexture(self):
        if self.components.profile:
            return self.components.profile["properties"][0]["value"]
        return None
    
    @headtexture.setter
    def headtexture(self, headtexture: str):
        self.components.profile = {"properties": [{"name": "texture", "value": headtexture}]}
    
    @property
    def item(self) -> str:
        return self._item
    
    @item.setter
    def item(self, item: str):
        self._item = item

    @property
    def enchantable(self) -> int:
        return self.components.enchantable["value"] or None
    
    @enchantable.setter
    def enchantable(self, enchantability: int):
        self.components.enchantable = {"value": enchantability}

    @property
    def rarity(self) -> int:
        return self.components.rarity or None
    
    @rarity.setter
    def rarity(self, rarity: str):
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")

    def damagable(self, max_durability: int, unbreakable: bool = False, break_sound: str = "intentionally_empty", repair_materials: list[str] = 0):
        self.components.break_sound = break_sound
        self.components.damage = 0
        self.components.max_damage = max_durability
        self.components.max_stack_size = 1
        self.components.repairable = {"items": repair_materials}
        if unbreakable:
            self.components.unbreakable = {}
        self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit

    
    def weapon(self, max_durability: int, attack_damage: float, attack_speed: float,  break_sound: str, repair_materials: list[str] = [], disable_blocking: int = 0, item_damage_per_attack: int = 1):
        self.damagable(max_durability=max_durability, break_sound=break_sound, repair_materials=repair_materials)
        self.components.attribute_modifier = self.components.attribute_modifier or [] # ersetzt alles was "falsy" ist (False, None, []).
        self.components.attribute_modifier.append({
                                        "id": "base_attack_damage",
                                        "amount": attack_damage - 1,
                                        "type": "minecraft:attack_damage",
                                        "operation": "add_value",
                                        "slot": "mainhand"
                                    })
        self.components.attribute_modifier.append({
                                        "id": "base_attack_speed",
                                        "amount": attack_speed - 4,
                                        "type": "minecraft:attack_speed",
                                        "operation": "add_value",
                                        "slot": "mainhand"
                                    })
        self.components.tool = {"rules": [], "can_destroy_blocks_in_creative": False}
        self.components.weapon = {"item_damage_per_attack": item_damage_per_attack, "disable_blocking_for_seconds": disable_blocking}
    

    def __iter__(self) -> dict:
        components = self.components.model_dump()

        # Remove components unset in the ItemComponents abstraction
        unset_components = [key for key, value in self.components.model_dump().items() if value is None]
        for component in unset_components:
            components.pop(component)
        
        # Remove components
        for component in self.removed_components:
            components[f"!{component}"] = {}
      
        return iter(components.items())
    
    def componentsJSON(self, indent: int = 4) -> str:
        return json.dumps(dict(self), indent=indent, ensure_ascii=False)