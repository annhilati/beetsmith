# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#
# TODO: Armor, Armorsets, Food, Abilities, Lore, load name and lore from stringified json or json files, rework environment_resistences()

import json
from .components import ItemComponents
from .lib import *
from beet import *

class CustomItem():
    "Data model representing a custom item. For details see the classes cosntructor"
    # Version: 1.21.5
    def __init__(self, id: str, name: str | dict, model: str, texture: str = None):
        """
        Data model representing a custom item

        #### Parameters
            - id (str): Namespaced id of the item for defining filenames
            - name (str | dict): Name of the item as a plain string or text component as a dict
            - model (str): Asset name of the items model
            - texture (str): Texture of the item if the model is 'minecraft:player_head' in encoded base64

        #### Templates (as Methods)
            - damagable
            - weapon
            - enchantable
            - environment_resistence

        #### Modifiers (as Memebrs)
            - headtexture (str)
            - rarity (str)
        """

        self.id: str = ensureResourceLocation(id)
        self.item: str = "minecraft:music_disc_11"
        "The custom items hardcoded item type"
        self.removed_components: list[str] = ["jukebox_playable"]
        "List of removed components"
        self.components = ItemComponents()
        "ItemComponent object of the custom item's components. They can be accessed and overwritten by setting `.components` members"
        self.tags: list[str] = []
        "List of tags the custom items needs to have including namespace"
        #self.additional_files = []

        self.components.item_name = name
        self.components.item_model = ensureResourceLocation(model)
        if texture:
            self.components.profile = {"properties": [{"name": "texture", "value": texture}]}
        self.components.max_stack_size = 64

    def damagable(self, max_durability: int, unbreakable: bool = False, break_sound: str = "entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
        """
        Set the custom items damagability properties

        #### Parameters:
            - max_durability (int): The amount of actions the item can perform until it breaks
            - unbreakable (bool): Whether the item cannot take damage from using it
            - break_sound (str): A [sound event](https://minecraft.wiki/w/Sounds.json#Sound_events) played when the item breaks
            - repair_materials (list[str]): List of materials, stated by item ids, which the item can be repaired with in an anvil
            - additional_repair_cost (int): Amount of experience levels additionally raised when repairing the item in an anvil 
        """
        if unbreakable: 
            self.components.unbreakable = {}
        else:
            self.components.break_sound = ensureResourceLocation(break_sound)
            self.components.damage = 0
            self.components.max_damage = max_durability
            self.components.repairable = {"items": repair_materials}
            self.components.repair_cost = additional_repair_cost
            self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit
        self.components.max_stack_size = 1

    def weapon(self, max_durability: int, attack_damage: float, attack_speed: float, break_sound: str, repair_materials: list[str] = [], disable_blocking: float = 0, item_damage_per_attack: int = 1):
        """
        Set the custom items weapon properties

        #### Parameters:
            - max_durability (int): The amount of actions the item can perform until it breaks
            - attack_damage (int): The amount of damage the item does including damage done by empty hand
            - attack_speed (int): The amount of fully charged attacks the item canperform per second
            - break_sound (str): A [sound event](https://minecraft.wiki/w/Sounds.json#Sound_events) played when the item breaks
            - repair_materials (list[str]): List of materials, stated by item ids, which the item can be repaired with in an anvil
            - disable_blocking (float): The number of seconds the item disables blocking for the enemy when hitting while the enemy is blocking
            - item_damage_per_attack (int): The amount of durability removed when performing an attack
        """
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
        self.tags.append("minecraft:swords")

    def enchantable(self, enchantability: int, enchantable_tag: str):
        """
        Sets the custom item's enchantability properties

        #### Parameters:
            - enchantability (int): Metric for how high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): A [tag that specifies what enchantments the item can get](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable) led by `enchantable/`
        """
        self.components.enchantable = {"value": enchantability}
        self.tags.append(ensureResourceLocation(enchantable_tag))
        # Needs to include enchantable/
    
    def rarity(self, rarity: str):
        "Sets the custom items rarity. One of `common`, `uncommon`, `rare` and `epic`"
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
        
    # def environment_resistence(self, fire: bool, explosions: bool):
    #     if fire and explosions:
    #         damageTypeTag = DamageTypeTag({
    #             "values": ["#minecraft:is_fire", "#minecraft:is_explosion"]
    #         })
    #         return damageTypeTag
    #     if fire:
    #         self.components.damage_resistent = {"types": "#minecraft:is_fire"}
    #     if explosions:
    #         self.components.damage_resistent = {"types": "#minecraft:is_explosion"}


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
    
    def componentsDict(self) -> dict:
        return dict(self)
    
    def componentsJSON(self, indent: int = 4) -> str:
        return json.dumps(self.componentsDict(), indent=indent, ensure_ascii=False)
    
    def generateLootTable(self) -> LootTable:
        "Generates a beet LootTable object. The loot table only contains the data about the custom item"
        # Version: 1.21.5
        json = {
            "pools": [
                {
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:item",
                            "name": self.item,
                            "functions": [
                                {
                                "function": "minecraft:set_components",
                                "components": dict(self)
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        lt = LootTable(json)
        return lt

    def generate_additional_files(self) -> list[AdditionalFile]:
        """
        Generates a list of AdditionalFile models, that have all neccesarry data as their members

            - type (class): A beet class for a file
            - name (str): The namespaced id of the file
            - content (dict): The files content
        """
        files = []
        for tag in self.tags:
            tagObj = {
                "replace": False,
                "values": [self.item]
            }
            files.append(AdditionalFile(type=ItemTag, name=ensureResourceLocation(tag), content=tagObj))

        return files
    
    def implement(self, datapack: DataPack) -> None:
        """
        Implement the custom item into a datapack
        """

        datapack[id] = self.generateLootTable()

        for file in self.generate_additional_files():
            datapack[file.name] = file.type(file.content)