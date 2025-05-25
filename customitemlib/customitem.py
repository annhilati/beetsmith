# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#

import json
import beet
import uuid
from typing import Literal
from .components import *
from .lib import *



class CustomItem():
    "Data model representing a custom item. For details see the classes cosntructor"
    def __init__(self, id: str, name: str | dict, model: str, texture: str = None):
        """
        Data model representing a custom item

        #### Parameters
            - id (str): Namespaced id of the item for meta files
            - name (str | dict): Name of the item as a plain string or text component as a dict
            - model (str): Asset name of the items model
            - texture (str): Texture of the item if the model is 'minecraft:player_head' in encoded base64

        #### Templates (as Methods)
            - damagable
            - enchantable
            - environment_resistance
            - headtexture (str)
            - rarity (str)
            - weapon
        """

        self.id = resourceLocation(id)
        "Namespaced id of the item for meta files"

        self.item: str = "minecraft:music_disc_11"
        "The custom items hardcoded item type"

        self.removed_components: list[str] = ["jukebox_playable"]
        "List of removed components"
        
        self.components = ItemComponents()
        "ItemComponent object of the custom item's components. They can be accessed and overwritten by setting `.components` members"
        
        self.tags: list[str] = []
        "List of item tags the custom items needs to have"

        self._additional_files: list[AdditionalFile] = []

        self.components.item_name = textComponent(name)
        self.components.custom_data = {"id": self.id}
        self.components.item_model = resourceLocation(model)
        self.components.max_stack_size = 64
        if texture:
            self.components.profile = {"properties": [{"name": "texture", "value": texture}]}

    # ╭────────────────────────────────────────────────────────────╮
    # │                          Templates                         │ 
    # ╰────────────────────────────────────────────────────────────╯
    
    def lore(self, textcomponent: str | dict | list) -> None:
        """Sets the custom items lore. The text component can be a string, a dict, a list or stringified JSON"""
        self.components.lore = textComponent(textcomponent)
    
    def damagable(self, max_durability: int, unbreakable: bool = False, break_sound: str = "minecraft:entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
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
            self.components.break_sound = resourceLocation(break_sound)
            self.components.damage = 0
            self.components.max_damage = max_durability
            self.components.repairable = {"items": [resourceLocation(item) for item in repair_materials]}
            self.components.repair_cost = additional_repair_cost
            self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit
        self.components.max_stack_size = 1

    def weapon(self, attack_damage: float, attack_speed: float, can_sweep: bool, disable_blocking: float = 0, item_damage_per_attack: int = 1):
        """
        Set the custom items weapon properties

        #### Parameters:
            - attack_damage (int): The amount of damage the item does including damage done by empty hand
            - attack_speed (int): The amount of fully charged attacks the item canperform per second
            - can_sweep (bool): Whether the weapon can perform sweep attacks
            - disable_blocking (float): The number of seconds the item disables blocking for the enemy when hitting while the enemy is blocking
            - item_damage_per_attack (int): The amount of durability removed when performing an attack
        """
        self.components.attribute_modifiers = self.components.attribute_modifiers or [] # ersetzt alles was "falsy" ist (False, None, []).
        self.components.attribute_modifiers.append({
                                        "id": "base_attack_damage",
                                        "amount": attack_damage - 1,
                                        "type": "minecraft:attack_damage",
                                        "operation": "add_value",
                                        "slot": "mainhand"
                                    })
        self.components.attribute_modifiers.append({
                                        "id": "base_attack_speed",
                                        "amount": attack_speed - 4,
                                        "type": "minecraft:attack_speed",
                                        "operation": "add_value",
                                        "slot": "mainhand"
                                    })
        self.components.weapon = {"item_damage_per_attack": item_damage_per_attack, "disable_blocking_for_seconds": disable_blocking}
        if can_sweep:
            self.components.tool = {"rules": [], "can_destroy_blocks_in_creative": False}
            self.tags.append("minecraft:swords")

    def enchantable(self, enchantability: int, enchantable_tag: str):
        """
        Sets the custom item's enchantability properties

        #### Parameters:
            - enchantability (int): Metric for how high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): A [tag that specifies what enchantments the item can get](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable)
                - No leading `#` required since this is not a tag refference 
                - Vanilla tags begin with `enchantable/` and are `armor`, `bow`, `chest_armor`, `crossbow`, `durability`, `equippable`, `fire_aspect`, `fishing`, `foot_armor`, `head_armor`, `leg_armor`, `mace`, `mining`, `mining_loot`, `sharp_weapon`, `sword`, `trident` and `weapon`
        """
        self.components.enchantable = {"value": enchantability}
        self.tags.append(resourceLocation(enchantable_tag)) # Needs to include enchantable/
    
    def rarity(self, rarity: Literal["common", "uncommon", "rare", "epic"]):
        "Sets the custom items rarity. One of `common`, `uncommon`, `rare` and `epic`"
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
        
    def environment_resistance(self, fire: bool, explosions: bool) -> None:
        if fire and explosions:
            tag_data = {"values": ["#minecraft:is_fire", "#minecraft:is_explosion"]}
            self._additional_files.append(AdditionalFile(registry=beet.DamageTypeTag, name=self.id, content=tag_data))
            self.components.damage_resistant = {"types": f"#{self.id}"}
        elif fire:
            self.components.damage_resistant = {"types": "#minecraft:is_fire"}
        elif explosions:
            self.components.damage_resistant = {"types": "#minecraft:is_explosion"}

    def right_click_ability(self, description: str | dict | list[dict | list], cooldown: int, function: str, cooldown_group: str = None):
        """
        **This feature is still experimentall and cause problems in combination with other items**

        Sets a right click ability for the custom item

        #### Parameters:
            - description (str | dict | list[dict | list]): A text component. Behaves exactly like lore but can't be empty
            - cooldown (int): The number of seconds the item can't be used again after using
            - function (str): A resource location of a function that is called when using the ability
            - cooldown (str): A group of items that share cooldown. Leave empty for this item to be unique
        """
        trigger_advancement = self.id.replace(":", ":ability/", 1)
        main_function = self.id.replace(":", ":ability/", 1)
        ability_function = resourceLocation(function)
        if not cooldown_group:
            cooldown_group = self.id
        cooldown_score = cooldown_group.replace(":", ".")
        
        self.item = "minecraft:goat_horn"

        self.components.instrument = {"range": 10, "description": textComponent(description), "sound_event": "minecraft:intentionally_empty", "use_duration": 0.001}
        
        self.components.use_cooldown = {"seconds": cooldown, "cooldown_group": resourceLocation(cooldown_group)}
    
        # Cooldown Checker Function
        self._additional_files.append(AdditionalFile(
            registry=beet.Function,
            name="customitemlib:load",
            content=[
                f"scoreboard objectives add {cooldown_score} dummy"
            ]
        ))
        self._additional_files.append(AdditionalFile(
            registry=beet.Function,
            name="customitemlib:cooldown",
            content=[
                f"execute as @a[scores={{{cooldown_score}=1..}}] run scoreboard players remove @s {cooldown_score} 1"
            ]
        ))
        self._additional_files.append(AdditionalFile(
            registry=beet.FunctionTag,
            name="minecraft:tick",
            content={
                "replace": False, "values": ["customitemlib:cooldown"]
            }
        ))
        self._additional_files.append(AdditionalFile(
            registry=beet.FunctionTag,
            name="minecraft:load",
            content={
                "replace": False, "values": ["customitemlib:load"]
            }
        ))

        # Ability Trigger Advancement
        self._additional_files.append(AdditionalFile(
            registry=beet.Advancement,
            name=trigger_advancement,
            content={
                "criteria": { "use_item": {
                    "trigger": "minecraft:using_item",
                    "conditions": { "item": { "predicates": {
                        "minecraft:custom_data": {"id": self.id}
                    }}}
                }},
                "rewards": { "function": main_function }
            }
        ))

        # Ability Main Function
        self._additional_files.append(AdditionalFile(
            registry=beet.Function,
            name=main_function,
            content=[
                f"execute if score @s {cooldown_score} matches 0 run function {ability_function}",
                f"advancement revoke @s only {trigger_advancement}",
                f"scoreboard players set @s {cooldown_score} {cooldown * 20}"
            ]
        ))

    # ╭────────────────────────────────────────────────────────────╮
    # │                        Implementation                      │ 
    # ╰────────────────────────────────────────────────────────────╯

    def __str__(self) -> str:
        return f"<CustomItem '{self.id}' ({self.item} with {len(self.component_data())} components)>"

    def component_data(self) -> dict:
        "Returns the custom items complete component data"
        components = self.components.model_dump()

        # Remove components unset in the ItemComponents abstraction
        unset_components = [key for key, value in self.components.model_dump().items() if value is None]
        for component in unset_components:
            components.pop(component)
        
        # Remove components
        for component in self.removed_components:
            components[f"!{component}"] = {}
      
        return components
    
    def components_json(self, indent: int = 4) -> str:
        "Returns a formatted stringified JSON of the complete component data"
        return json.dumps(self.component_data(), indent=indent, ensure_ascii=False)
    
    def loot_table(self) -> beet.LootTable:
        "Returns a minimal beet loot table object of the custom item with all component data"
        # Version: 1.21.5
        json = {
            "pools": [{
                "rolls": 1,
                "entries": [{
                    "type": "minecraft:item",
                    "name": self.item,
                    "functions": [{
                        "function": "minecraft:set_components",
                        "components": self.component_data()
        }]}]}]}
        
        return beet.LootTable(json)

    def additional_files(self) -> list[AdditionalFile]:
        """
        Generates a list of AdditionalFile models, that have all neccesarry data as their members

            - type (class): A beet class for a file
            - name (str): The namespaced id of the file
            - content (dict): The files content
        """
        files = []
        for tag in self.tags:
            tag_data = {"replace": False, "values": [self.item]}
            files.append(AdditionalFile(registry=beet.ItemTag, name=tag, content=tag_data))

        files.extend(self._additional_files)

        return files
    
    def implement(self, datapack: beet.DataPack) -> None:
        """
        Implement the custom item into a beet datapack
        """

        # Loot Table
        datapack[self.id] = self.loot_table()

        for file in self.additional_files():
            if file.registry == beet.FunctionTag:
                datapack.function_tags.setdefault(file.name).merge(file.registry(file.content)) # Can either merge or create function tags
            if file.registry == beet.Function:
                datapack.functions.setdefault(file.name).append(file.registry(file.content)) # Can either merge or create functions
            else:
                datapack[file.name] = file.registry(file.content)