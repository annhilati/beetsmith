# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#

import json
import yaml
import beet
import uuid
import warnings
import pathlib
from typing import Literal
from .components import *
from .lib import *

__minecraft_game_version__ = "1.21.5"
__minecraft_data_version__ = 71

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
        
        self.required_tags: list[str] = []
        "List of item tags the custom items hardcoded item needs to have"

        self._additional_required_files: list[RegistryFile] = []

        self.components.item_name = textComponent(name)
        self.components.custom_data = {"id": self.id}
        self.components.item_model = resourceLocation(model)
        self.components.max_stack_size = 64
        if texture:
            self.components.profile = {"properties": [{"name": "texture", "value": texture}]}

    def __str__(self) -> str:
        return f"<CustomItem '{self.id}' ('{self.item}' with {len(self.components_data)} components and {len(self.required_files)} additional files needed)>"
    
    # ╭────────────────────────────────────────────────────────────╮
    # │                          Templates                         │ 
    # ╰────────────────────────────────────────────────────────────╯
    
    def set_damagable(self, durability: int, unbreakable: bool = False, break_sound: str = "minecraft:entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
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
            self.components.max_damage = durability
            self.components.repairable = {"items": [resourceLocation(item) for item in repair_materials]}
            self.components.repair_cost = additional_repair_cost
            self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit
        self.components.max_stack_size = 1

    def set_enchantable(self, enchantability: int, enchantable_tag: str):
        """
        Sets the custom item's enchantability properties

        #### Parameters:
            - enchantability (int): Metric for how high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): A [tag that specifies what enchantments the item can get](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable)
                - No leading `#` required since this is not a tag refference 
                - Vanilla tags begin with `enchantable/` and are `armor`, `bow`, `chest_armor`, `crossbow`, `durability`, `equippable`, `fire_aspect`, `fishing`, `foot_armor`, `head_armor`, `leg_armor`, `mace`, `mining`, `mining_loot`, `sharp_weapon`, `sword`, `trident` and `weapon`
        """
        self.components.enchantable = {"value": enchantability}
        self.required_tags.append(resourceLocation(enchantable_tag)) # Needs to include enchantable/
    
    def set_environment_resistance(self, fire: bool, explosions: bool) -> None:
        if fire and explosions:
            tag_data = {"values": ["#minecraft:is_fire", "#minecraft:is_explosion"]}
            self._additional_required_files.append(RegistryFile(registry=beet.DamageTypeTag, name=self.id, content=tag_data))
            self.components.damage_resistant = {"types": f"#{self.id}"}
        elif fire:
            self.components.damage_resistant = {"types": "#minecraft:is_fire"}
        elif explosions:
            self.components.damage_resistant = {"types": "#minecraft:is_explosion"}

    def set_lore(self, textcomponent: str | dict | list) -> None:
        """Sets the custom items lore. The text component can be a string, a dict, a list or stringified JSON"""
        self.components.lore = textComponent(textcomponent)

    def set_rarity(self, rarity: Literal["common", "uncommon", "rare", "epic"]):
        "Sets the custom items rarity. One of `common`, `uncommon`, `rare` and `epic`"
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
        
    def set_right_click_ability(self, description: str | dict | list[dict | list], cooldown: int, function: str, cooldown_group: str = uuid.UUID):
        """
        **This feature is still experimentall and may cause problems in combination with other items**

        Sets a right click ability for the custom item

        #### Parameters:
            - description (str | dict | list[dict | list]): A text component. Behaves exactly like lore but can't be empty
            - cooldown (int): The number of seconds the item can't be used again after using
            - function (str): A resource location of a function that is called when using the ability
            - cooldown_group (str): A group of items that share cooldown.
                1. default: The item will share cooldown time with all items of the same type
                2. (str): The item will share cooldown time with all items of this cooldown group
                3. (None): Each instance of the item will have it's own unique cooldown
        """

        if cooldown_group == uuid.UUID:
            cooldown_group = self.id

        trigger_advancement = self.id.replace(":", ":ability/", 1)
        main_function = self.id.replace(":", ":ability/", 1)
        ability_function = resourceLocation(function)

        cooldown_score = cooldown_group.replace(":", ".cooldown.")
        
        self.item = "minecraft:goat_horn"

        self.components.instrument = {"range": 10, "description": textComponent(description), "sound_event": "minecraft:intentionally_empty", "use_duration": 0.001}
        
        self.components.use_cooldown = {"seconds": cooldown, "cooldown_group": cooldown_group}
    
        # Cooldown Checker Function
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name="customitemlib:load",
            content=[
                f"scoreboard objectives add {cooldown_score} dummy"
            ]
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name="customitemlib:cooldown",
            content=[
                f"execute as @a[scores={{{cooldown_score}=1..}}] run scoreboard players remove @s {cooldown_score} 1"
            ]
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.FunctionTag,
            name="minecraft:tick",
            content={
                "replace": False, "values": ["customitemlib:cooldown"]
            }
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.FunctionTag,
            name="minecraft:load",
            content={
                "replace": False, "values": ["customitemlib:load"]
            }
        ))

        # Ability Trigger Advancement
        self._additional_required_files.append(RegistryFile(
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
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name=main_function,
            content=[
                f"execute if score @s {cooldown_score} matches 0 run function {ability_function}",
                f"advancement revoke @s only {trigger_advancement}",
                f"scoreboard players set @s {cooldown_score} {cooldown * 20}"
            ]
        ))

    def set_attribute_modifier(self, attribute: str, slot: str, value: float, operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"], id: str = None) -> None:
        """
        Adds a attribute modifier to the custom item

        #### Parameters:
            - attribute (str): The [name of the attribute](https://minecraft.wiki/w/Attribute#Attributes) to be modified
            - slot (str): The slot where the modifier takes action (`any`, `hand`, `armor`, `mainhand`, `offhand`, `head`, `chest`, `legs`, `feet` or `body`)
            - value (float): The amount or factor to modify the attribute with
            - operation (str): How the value is to be [applied mathmatically](https://minecraft.wiki/w/Attribute#Modifiers)
            - id (str): [Identifier](https://minecraft.wiki/w/Attribute#Vanilla_modifiers) of the modifier. Leave empty for it to be unique
        """
        if id is None:
            id = str(uuid.uuid4())
        self.components.attribute_modifiers = self.components.attribute_modifiers or [] # ersetzt alles was "falsy" ist (False, None, []).
        self.components.attribute_modifiers.append({
                                        "id": id,
                                        "amount": value,
                                        "type": attribute,
                                        "operation": operation,
                                        "slot": slot
                                    })
        
    def set_weapon(self, attack_damage: float, attack_speed: float, can_sweep: bool, disable_blocking: float = 0, item_damage_per_attack: int = 1):
        """
        Set the custom items weapon properties

        #### Parameters:
            - attack_damage (int): The amount of damage the item does including damage done by empty hand
            - attack_speed (int): The amount of fully charged attacks the item canperform per second
            - can_sweep (bool): Whether the weapon can perform sweep attacks
            - disable_blocking (float): The number of seconds the item disables blocking for the enemy when hitting while the enemy is blocking
            - item_damage_per_attack (int): The amount of durability removed when performing an attack
        """
        self.set_attribute_modifier(attribute="minecraft:attack_damage",
                                value=attack_damage - 1,
                                slot="mainhand",
                                operation="add_value",
                                id="base_attack_damage"
                                )
        self.set_attribute_modifier(attribute="minecraft:attack_speed",
                                value=attack_speed - 4,
                                slot="mainhand",
                                operation="add_value",
                                id="base_attack_speed")
        self.components.weapon = {"item_damage_per_attack": item_damage_per_attack, "disable_blocking_for_seconds": disable_blocking}
        if can_sweep:
            self.components.tool = {"rules": [], "can_destroy_blocks_in_creative": False}
            self.required_tags.append("minecraft:swords")

    # ╭────────────────────────────────────────────────────────────╮
    # │                        Implementation                      │ 
    # ╰────────────────────────────────────────────────────────────╯

    @property
    def components_data(self) -> dict:
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
        return json.dumps(self.components_data, indent=indent, ensure_ascii=False)
    
    @property
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
                        "components": self.components_data
        }]}]}]}
        
        return beet.LootTable(json)

    @property
    def required_files(self) -> list[RegistryFile]:
        """
        Generates a list of RegistryEntry objects, that have all neccesarry data for a file

            - registry (class): A beet class for a file
            - name (str): The namespaced id of the file
            - content (dict | list[str]): The files content
        """
        files = []

        # Tags
        for tag in self.required_tags:
            tag_data = {"replace": False, "values": [self.item]}
            files.append(RegistryFile(registry=beet.ItemTag, name=tag, content=tag_data))

        # Explicitely needed files
        files.extend(self._additional_required_files)

        return files
    
    def implement(self, datapack: beet.DataPack) -> None:
        """
        Implement the custom item into a beet datapack
        """

        pack_format = datapack.pack_format
        if pack_format != __minecraft_data_version__:
            warnings.warn(f"The datapack does not have the main pack format {__minecraft_data_version__}! Some content may not be loaded by Minecraft!", category=UserWarning)

        # Loottable
        datapack[self.id.replace(":", ":item/", 1)] = self.loot_table

        # Required Files
        for file in self.required_files:

            if file.registry == beet.FunctionTag:
                datapack.function_tags.setdefault(file.name).merge(file.registry(file.content)) # Can either merge or create function tags
            
            if file.registry == beet.Function:
                datapack.functions.setdefault(file.name).append(file.registry(file.content)) # Can either merge or create functions
            
            else:
                datapack[file.name] = file.registry(file.content)

    def create_from_yaml(path: str):
        """
        Creates a CustomItem object from a file in a certain yaml based definition format
        """

        with open(path, 'r') as f:
            data: dict = yaml.safe_load(f)

        item = CustomItem(id=data["id"], name=data["name"], model=data["model"], texture=data.get("texture"))

        for method_name, args in data["templates"].items():
            method = getattr(item, method_name, None)
            if method is None or not callable(method):
                raise ValueError(f"'{method_name}' is not a valid template")
            if not isinstance(args, dict):
                raise ValueError(f"Arguments for '{method_name}' have to be in a key-value format")
            method(**args)

        return item

def load_dir_and_implement(directory: str, datapack: beet.DataPack) -> None:
    """
    Looks for yaml files in a directory and implements all of them into a contexts datapack

    #### Parameters:
        - ctx (Context): A beet pipeline context
        - directory (str): Directory path in the contexts directory
    """
    directory = pathlib.Path(directory)
    files = [str(p) for p in directory.glob("*.yml")] + [str(p) for p in directory.glob("*.yaml")]

    for file in files:
        try: 
            item: CustomItem = CustomItem.create_from_yaml(file)
            item.implement(datapack)

        except Exception as e:
            warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)