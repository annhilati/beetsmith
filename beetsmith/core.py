# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#

import json
import beet
import uuid
import warnings
from typing import Literal
from .models import *
from .validation import *
from ._internal.lib import *

__minecraft_game_version__ = "1.21.5"
__minecraft_data_version__ = 71
technical_namespace = "beetsmith"
generated_file_pattern = "{technical_namespace}:{namespace}/{thing}/{id}"

class CustomItem():
    "Data model representing a custom item. For details see the classes constructor"
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

        self._namespace = self.id.split(":")[0]
        self._loose_id = self.id.split(":")[1]


        self._applied_methods: list[str] = []
        
        self.required_tags: list[str] = []
        "List of item tags the custom items hardcoded item needs to have"

        self._additional_required_files: list[RegistryFile] = []
        "Info: These are not all files! Use self._required_files"
        
        self.item: str = "minecraft:music_disc_11"
        "The custom items hardcoded item type"

        self.components = ItemComponents()
        "ItemComponent object of the custom item's components. They can be accessed and overwritten by setting `.components` members"
        self.components.item_name = textComponent(name)[0]
        self.components.custom_data = {"id": self.id}
        self.components.item_model = resourceLocation(model)
        self.components.max_stack_size = 64
        if texture:
            self.components.profile = {"properties": [{"name": "texture", "value": texture}]}
        self.removed_components: list[str] = ["jukebox_playable"]
        "List of removed components"

    def __str__(self) -> str:
        return f"<CustomItem '{self.id}' ('{self.item}' with {len(self._components_data)} components and {len(self._required_files)} additional files needed)>"
    
    # ╭────────────────────────────────────────────────────────────╮
    # │                           Methods                          │ 
    # ╰────────────────────────────────────────────────────────────╯

    def attribute_modifier(self, attribute: str, slot: str, value: float, operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"], id: str = None) -> None:
        """
        Adds a attribute modifier to the custom item

        #### Parameters:
            - attribute (str): The [name of the attribute](https://minecraft.wiki/w/Attribute#Attributes) to be modified
            - slot (str): The slot where the modifier takes action (`any`, `hand`, `armor`, `mainhand`, `offhand`, `head`, `chest`, `legs`, `feet` or `body`)
            - value (float): The amount or factor to modify the attribute with
            - operation (str): How the value is to be [applied mathmatically](https://minecraft.wiki/w/Attribute#Modifiers)
            - id (str): [Identifier](https://minecraft.wiki/w/Attribute#Vanilla_modifiers) of the modifier. Leave empty for it to be unique
        """
        self._applied_methods.append("attribute_modifier")

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
        
    def consumable(self,
                   time: float,
                   animation: Literal["none", "eat", "drink", "block", "bow", "spear", "crossbow", "spyglass", "toot_horn" "brush"],
                   nutrition: int,
                   saturation: float,
                   consume_always: bool,
                   particles: bool,
                   effects: list[dict],
                   sound: str = "entity.generic.eat"):
        """
        Adds consumption behaviour to the custom item

        #### Parameters:
            - time (float): Number of seconds the consumption takes
            - animation (str): Animation to play while consuming the item
            - nutrition (int): Amount of hunger to regenerate on consumption
            - saturation (float): Amount of saturation to add on consumption
            - consume_always (bool): Whether the item can be consumed even if nutrition is full
            - particles (bool): Whether to create particles on consumption
            - effects (list[dict]): List of [effects](https://minecraft.wiki/w/Data_component_format/consumable) taking place on consumption
            - sound (str): Resource location of a sound event which shall be played while consuming the item
        """
        self._applied_methods.append("consumable")
        self.components.consumable = {
            "consume_seconds": time,
            "animation": animation,
            "sound": resourceLocation(sound),
            "has_consume_particles": particles,
            "on_consume_effects": effects
        }
        self.components.food = {
            "nutrition": nutrition,
            "saturation": saturation,
            "can_always_eat": consume_always
        }
    
    def damagable(self, durability: int, unbreakable: bool = False, break_sound: str = "minecraft:entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
        """
        Set the custom items damagability properties

        #### Parameters:
            - durability (int): The amount of actions the item can perform until it breaks
            - unbreakable (bool): Whether the item cannot take damage from using it
            - break_sound (str): A [sound event](https://minecraft.wiki/w/Sounds.json#Sound_events) played when the item breaks
            - repair_materials (list[str]): List of materials, stated by item ids, which the item can be repaired with in an anvil
            - additional_repair_cost (int): Amount of experience levels additionally raised when repairing the item in an anvil 
        """
        self._applied_methods.append("damagable")
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

    def enchantable(self, enchantability: int, enchantable_tag: str):
        """
        Sets the custom item's enchantability properties

        #### Parameters:
            - enchantability (int): Metric for how high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): A [tag that specifies what enchantments the item can get](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable)
                - No leading `#` required since this is not a tag refference 
                - Vanilla tags begin with `enchantable/` and are `armor`, `bow`, `chest_armor`, `crossbow`, `durability`, `equippable`, `fire_aspect`, `fishing`, `foot_armor`, `head_armor`, `leg_armor`, `mace`, `mining`, `mining_loot`, `sharp_weapon`, `sword`, `trident` and `weapon`
        """
        self._applied_methods.append("enchantable")
        self.components.enchantable = {"value": enchantability}
        self.required_tags.append(resourceLocation(enchantable_tag)) # Needs to include enchantable/
    
    def environment_resistance(self, fire: bool, explosions: bool) -> None:
        self._applied_methods.append("environment_resistance")
        if fire and explosions:
            tag_data = {"values": ["#minecraft:is_fire", "#minecraft:is_explosion"]}
            self._additional_required_files.append(RegistryFile(registry=beet.DamageTypeTag, name=self.id, content=tag_data))
            self.components.damage_resistant = {"types": f"#{self.id}"}
        elif fire:
            self.components.damage_resistant = {"types": "#minecraft:is_fire"}
        elif explosions:
            self.components.damage_resistant = {"types": "#minecraft:is_explosion"}

    def lore(self, textcomponent: str | dict | list) -> None:
        self._applied_methods.append("lore")
        """Sets the custom items lore. The text component can be a string, a dict, a list or stringified JSON"""
        self.components.lore = textComponent(textcomponent)

    def rarity(self, rarity: Literal["common", "uncommon", "rare", "epic"]):
        self._applied_methods.append("rarity")
        "Sets the custom items rarity. One of `common`, `uncommon`, `rare` and `epic`"
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
        
    def right_click_ability(self, description: str | dict | list[dict | list], cooldown: int, function: str, cooldown_group: str = uuid.UUID):
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
        self._applied_methods.append("right_click_ability")

        self.item = "minecraft:goat_horn"

        if cooldown_group == uuid.UUID:
            cooldown_group = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._namespace, thing="cooldown", id=self._loose_id)
        cooldown_name = cooldown_group.replace(":", ".").replace("/", ".")
        self.components.use_cooldown = {"seconds": cooldown, "cooldown_group": cooldown_group}
        
        self.components.instrument = {"range": 10, "description": textComponent(description), "sound_event": "minecraft:intentionally_empty", "use_duration": 0.001}
    
        ability_name = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._namespace, thing="ability", id=self._loose_id) # e.g. 'customitemlib:lategame/ability/hunter_sword'
        ability_function = resourceLocation(function)

        # Cooldown Checker Function
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name=f"{technical_namespace}:load",
            content=[
                f"scoreboard objectives add {cooldown_name} dummy"
            ]
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name=f"{technical_namespace}:cooldown",
            content=[
                f"execute as @a[scores={{{cooldown_name}=1..}}] run scoreboard players remove @s {cooldown_name} 1"
            ]
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.FunctionTag,
            name="minecraft:tick",
            content={
                "replace": False, "values": [f"{technical_namespace}:cooldown"]
            }
        ))
        self._additional_required_files.append(RegistryFile(
            registry=beet.FunctionTag,
            name="minecraft:load",
            content={
                "replace": False, "values": [f"{technical_namespace}:load"]
            }
        ))

        # Ability Trigger Advancement
        self._additional_required_files.append(RegistryFile(
            registry=beet.Advancement,
            name=ability_name,
            content={
                "criteria": { "use_item": {
                    "trigger": "minecraft:using_item",
                    "conditions": { "item": { "predicates": {
                        "minecraft:custom_data": {"id": self.id}
                    }}}
                }},
                "rewards": { "function": ability_name }
            }
        ))

        # Ability Main Function
        self._additional_required_files.append(RegistryFile(
            registry=beet.Function,
            name=ability_name,
            content=[
                f"execute if score @s {cooldown_name} matches 0 run function {ability_function}",
                f"advancement revoke @s only {ability_name}",
                f"scoreboard players set @s {cooldown_name} {cooldown * 20}"
            ]
        ))

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
        self._applied_methods.append("weapon")
        self.attribute_modifier(attribute="minecraft:attack_damage",
                                value=attack_damage - 1,
                                slot="mainhand",
                                operation="add_value",
                                id="base_attack_damage"
                                )
        self.attribute_modifier(attribute="minecraft:attack_speed",
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
    def _components_data(self) -> dict:
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
        return json.dumps(self._components_data, indent=indent, ensure_ascii=False)
    
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
                        "components": self._components_data
        }]}]}]}
        
        return beet.LootTable(json)

    @property
    def _required_files(self) -> list[RegistryFile]:
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
        if "right_click_ability" and "consumable" in self._applied_methods:
            warnings.warn(f"The custom item has two different right-clik-behaviours (consumption and ability) which will lead to incompatibilities")

        pack_format = datapack.pack_format
        if pack_format != __minecraft_data_version__:
            warnings.warn(f"The datapack does not have the main pack format {__minecraft_data_version__}! Some content may not be loaded by Minecraft!", category=UserWarning)

        # Loottable
        datapack[self.id.replace(":", ":item/", 1)] = self.loot_table

        # Required Files
        for file in self._required_files:

            if file.registry == beet.FunctionTag:
                datapack.function_tags.setdefault(file.name).merge(file.registry(file.content)) # Can either merge or create function tags
            
            if file.registry == beet.Function:
                datapack.functions.setdefault(file.name).append(file.registry(file.content)) # Can either merge or create functions
            
            else:
                datapack[file.name] = file.registry(file.content)

class ArmorSet():
    def __init__(self, ids: str, names: str = None, nouns: list[str] = ["Helmet", "Chestplate", "Leggings", "Boots"]):
        """
        Data model representing an armor set

        #### Parameters
            -
        """
        self.items = [
            CustomItem(ids.format(noun=nouns[0].lower()), names.format(noun=nouns[0]), "minecraft:diamond_helmet"),
            CustomItem(ids.format(noun=nouns[1].lower()), names.format(noun=nouns[1]), "minecraft:diamond_chestplate"),
            CustomItem(ids.format(noun=nouns[2].lower()), names.format(noun=nouns[2]), "minecraft:diamond_leggings"),
            CustomItem(ids.format(noun=nouns[3].lower()), names.format(noun=nouns[3]), "minecraft:diamond_boots"),
        ]