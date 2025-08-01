# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#

import json
import beet
import uuid
import inspect
import warnings
import functools
from typing import Literal, Union, Protocol, runtime_checkable
from dataclasses import dataclass, field, InitVar
from beetsmith.library.text_components import TextComponent
from beetsmith.library.validation import *
from beetsmith.library.utils import *
from beetsmith.core.models import *

__minecraft_game_version__ = "1.21.5"
__minecraft_data_version__ = 71
technical_namespace = "beetsmith"
generated_file_pattern = "{technical_namespace}:{namespace}/{thing}/{id}"

armor_slots = ("head", "chest", "legs", "feet")
be_trimmable_ids = ("minecraft:chainmail_helmet", "minecraft:chainmail_chestplate", "minecraft:chainmail_leggings", "minecraft:chainmail_boots")

_registered_implementations: set[tuple[str, beet.DataPack]] = set()

def log_duplicates(func):
    "Watches implemented custom item's ids on `_registered_implementations` and warns on duplicates."
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        id: str = getattr(self, "id", None)

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        datapack: beet.DataPack = bound.arguments.get("datapack")

        if (id, datapack) in _registered_implementations:
            warnings.warn(f"Multiple custom items with the id '{id}' were implemented")
        else:
            _registered_implementations.add((id, datapack))

        return func(*args, **kwargs)
    return wrapper

def behavior(function):
    "Appends the decorated function to self._applied_behaviours when it is called"
    def wrapper(self, *args, **kwargs):
        self._applied_behaviours.append(function.__name__)
        return function(self, *args, **kwargs)
    return wrapper

@runtime_checkable
class Implementable(Protocol):
    "Protocol for types with a `implement` method"
    def implement(self, datapack: beet.DataPack) -> None: ...

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                  CustomItem                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

@dataclass
class CustomItem:
    id: str
    name: Union[str, dict, list]
    model: str
    texture: str = None

    item:                       str                             = field(init=False, default="minecraft:music_disc_11")
    required_tags:              list[str]                       = field(init=False, default_factory=list)
    removed_components:         list[str]                       = field(init=False, default_factory=lambda: ["jukebox_playable"])
    components:                 ItemComponents                  = field(init=False)
    _id_namespace:              str                             = field(init=False)
    _id_short:                  str                             = field(init=False)
    _special_required_files:    list[tuple[str, beet.TextFile]] = field(init=False, default_factory=list)
    _applied_behaviours:        list                            = field(init=False, default_factory=list)

    def __post_init__(self):
        self.id = resourceLocation(self.id)
        self.components = ItemComponents()
        self.components.item_name = TextComponent.normalize(self.name)[0]
        self.components.custom_data = {"id": self.id}
        self.components.item_model = resourceLocation(self.model)
        self.components.max_stack_size = 64
        self.components.unbreakable = {}
        if self.texture:
            self.components.profile = {
                "properties": [{"name": "texture", "value": self.texture}]
            }
        self._id_namespace = self.id.split(":")[0]
        self._id_short = self.id.split(":")[1]

    def __str__(self) -> str:
        return f"<CustomItem '{self.id}' ('{self.item}' with {len(self._components_data)} components and {len(self.required_files)} additional files needed)>"

    # ╭────────────────────────────────────────────────────────────╮
    # │                          Behaviors                         │ 
    # ╰────────────────────────────────────────────────────────────╯

    @behavior
    def add_attribute_modifier(self, *,
                               attribute: str,
                               slot: Literal["any", "hand", "armor", "mainhand", "offhand", "head", "chest", "legs", "feet", "body"],
                               value: float, operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"],
                               id: str = uuid.UUID) -> None:
        """Adds a attribute modifier to the custom item.

        #### Parameters:
            - attribute (str): Name of the modified attribute [[Wiki](https://minecraft.wiki/w/Attribute#Attributes)]
            - slot (str): Slot where the modifier takes action
            - value (float): Amount or factor the attribute is modified with
            - operation (str): How the value is to be applied [[Wiki](https://minecraft.wiki/w/Attribute#Modifiers)]
            - id (str): Identifier of the modifier
                - Modifiers with the same identifier will overwrite each other
                - Some behaviours require specific identifiers [[Wiki](https://minecraft.wiki/w/Attribute#Vanilla_modifiers)]
        """
        if id is uuid.UUID:
            id = str(uuid.uuid4())
        self.components.attribute_modifiers.append({
            "id": id,
            "amount": value,
            "type": attribute,
            "operation": operation,
            "slot": slot
        })

    @behavior 
    def consumable(self, *,
                   time: float,
                   animation: Literal["none", "eat", "drink", "block", "bow", "spear", "crossbow", "spyglass", "toot_horn", "brush"],
                   nutrition: int,
                   saturation: float,
                   consume_always: bool,
                   particles: bool,
                   effects: list[dict] = [],
                   sound: str = "minecraft:entity.generic.eat",
                   cooldown: int = None,
                   cooldown_group: str = None,
                   function: str = None):
        """Adds consumption behaviour to the custom item.

        #### Parameters:
            - time (float): Number of seconds the consumption takes
            - animation (str): Animation played while consuming the item
            - nutrition (int): Amount of hunger regenerated after consumption
            - saturation (float): Amount of saturation added after consumption
            - consume_always (bool): Whether the item can be consumed even if nutrition is full
            - particles (bool): Whether to create particles while consuming
            - sound (str): Sound event played while consuming
            - cooldown (int): Number of seconds the item can't be used again after using
            - cooldown_group (str): Group of items that share the cooldown with this item
                1. default: The item will share cooldown time with all items of the same type
                2. (str): The item will share cooldown time with all items of this cooldown group
                3. (None): Each instance of the item will have it's own unique cooldown
            - effects (list[dict]): List of effects taking place after consumption [[Wiki](https://minecraft.wiki/w/Data_component_format/consumable)]
            - function (str): Function that is called when using the ability
        """
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
        if cooldown is not None:
            if cooldown_group == uuid.UUID:
                cooldown_group = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._id_namespace, thing="cooldown", id=self._id_short)
            self.components.use_cooldown = {"seconds": cooldown, "cooldown_group": cooldown_group}
        if function is not None:
            ability_name = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._id_namespace, thing="ability", id=self._id_short)
            ability_function = resourceLocation(function)
            files = [
                (
                    ability_name,
                    beet.Advancement({
                        "criteria": { "use_item": {
                            "trigger": "minecraft:using_item",
                            "conditions": { "item": { "predicates": {
                                "minecraft:custom_data": {"id": self.id}
                            }}}
                        }},
                        "rewards": { "function": ability_name }
                    })
                ),
                (
                ability_name,
                    beet.Function([
                        f"function {ability_function}",
                        f"advancement revoke @s only {ability_name}",
                    ])
                )
            ]
            self._special_required_files.extend(files)
    
    @behavior
    def damagable(self, *, durability: int, break_sound: str = "minecraft:entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
        """Adds damagability behaviour to the custom item.

        #### Parameters:
            - durability (int): Amount of actions the item can perform until it breaks
            - break_sound (str): Sound event played when the item breaks
            - repair_materials (list[str]): List of items which can be used in an anvil to restore durability
            - additional_repair_cost (int): Amount of experience levels additionally raised when repairing the item in an anvil 
        """        
        self.components.unbreakable = None
        self.components.break_sound = resourceLocation(break_sound)
        self.components.damage = 0
        self.components.max_damage = durability
        self.components.repairable = {"items": repair_materials}
        self.components.repair_cost = additional_repair_cost
        self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit
        self.components.max_stack_size = 1

    @behavior
    def enchantable(self, enchantability: int, enchantable_tag: str):
        """Adds enchantability behavior to the custom item.

        #### Parameters:
            - enchantability (int): How high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): Tag that specifies what enchantments the item can get [[Examples](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable)]
                - No leading `#` required since this is not a tag refference 
                - Vanilla tags begin with `enchantable/` and are `armor`, `bow`, `chest_armor`, `crossbow`, `durability`, `equippable`, `fire_aspect`, `fishing`, `foot_armor`, `head_armor`, `leg_armor`, `mace`, `mining`, `mining_loot`, `sharp_weapon`, `sword`, `trident` and `weapon`
        """
        self.components.enchantable = {"value": enchantability}
        self.required_tags.append(resourceLocation(enchantable_tag)) # Needs to include enchantable/
    
    @behavior
    def damage_resistance(self, damage_types: list[str]) -> None:
        """Sets which damage types the custom item (as item entity or as equippable when the wearer takes damage) is immune to.

        #### Parameters
            - damage_types (list[str]): A list of damage type tags (without leading `#`) [[Wiki](https://minecraft.wiki/w/Damage_type_tag_(Java_Edition)#List_of_tags)]
        
        """
        if len(damage_types) > 1:
            tag_data = {"values": [f"#{damage_type}" for damage_type in damage_types]}
            self._special_required_files.append((self.id, beet.DamageTypeTag(tag_data)))
            self.components.damage_resistant = {"types": f"#{self.id}"}
        else:
            self.components.damage_resistant = {"types": f"#{damage_types[0]}"}

    @behavior
    def equippable(self, *,
                   slot: Literal["head", "chest", "legs", "feet", "body"],
                   asset: str,
                   equip_sound: str = "minecraft:item.armor.equip_generic",
                   glider: bool = False,
                   dispensable: bool = True,
                   swappable: bool = True,
                   damage_on_hurt: bool = True,
                   equip_on_interaction: bool = False,
                   color: int = None) -> None:
        """Adds equippability behavior to the custom item.

        #### Parameters
            - slot (str): Slot the item can be equipped in
            - asset (str): Equipment asset [[Wiki](https://minecraft.wiki/w/Equipment)] [[Examples](https://mcasset.cloud/1.21.5/assets/minecraft/equipment)]
            - equip_sound (str): Sound event played when equipping the item
            - glider (bool): Whether the item makes the player fly like with an elytra when equipped
            - dispensable (bool): Whether the item can be equipped on entities by a dispenser
            - swappable (bool): Whether the item can be swapped with the item in the slot in can be equpped in by right clicking
            - damage_on_hurt (bool): Whether the item looses durability when the wearing entity is hurt
            - equip_on_interaction (bool): Whether the item can be equipped on an entity by right clicking it
            - color (int): Color value of the equippable if the equipment asset can be dyed
        """
        self.components.equippable = {
                "slot": slot,
                "equip_sound": equip_sound,
                "asset_id": resourceLocation(asset),
                "allowed_entities": [],
                "dispensable": dispensable,
                "swappable": swappable,
                "damage_on_hurt": damage_on_hurt,
                "equip_on_interact": equip_on_interaction
            }
        if glider:
            self.components.glider = {}
        if color:
            self.components.dyed_color = color

    @behavior
    def lore(self, textcomponent: str | dict | list) -> None:
        "Sets the custom items lore."
        self.components.lore = TextComponent.normalize(textcomponent)

    @behavior
    def rarity(self, rarity: Literal["common", "uncommon", "rare", "epic"]):
        "Sets the custom items rarity."
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
    
    @behavior
    def right_click_ability(self, *, description: str | dict | list, cooldown: int, function: str, cooldown_group: str = uuid.UUID):
        """Adds right click behavior to the custom item.

        #### Parameters:
            - description (str | dict | list): Text component displayed under the item's name
            - cooldown (int): Number of seconds the item can't be used again after using
            - function (str): Function that is called when using the ability
            - cooldown_group (str): Group of items that share the cooldown with this item
                1. default: The item will share cooldown time with all items of the same type
                2. (str): The item will share cooldown time with all items of this cooldown group
                3. (None): Each instance of the item will have it's own unique cooldown
        """
        self.item = "minecraft:goat_horn"

        if cooldown_group == uuid.UUID:
            cooldown_group = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._id_namespace, thing="cooldown", id=self._id_short)
        self.components.use_cooldown = {"seconds": cooldown, "cooldown_group": cooldown_group}
        
        self.components.instrument = {"range": 10, "description": TextComponent.normalize(description), "sound_event": "minecraft:intentionally_empty", "use_duration": 0.001}
    
        ability_name = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._id_namespace, thing="ability", id=self._id_short) # e.g. 'customitemlib:lategame/ability/hunter_sword'
        ability_function = resourceLocation(function)

        files = [
            (
                ability_name,
                beet.Advancement({
                    "criteria": { "use_item": {
                        "trigger": "minecraft:using_item",
                        "conditions": { "item": { "predicates": {
                            "minecraft:custom_data": {"id": self.id}
                        }}}
                    }},
                    "rewards": { "function": ability_name }
                })
            ),
            (
                ability_name,
                beet.Function([
                    f"data modify storage beetsmith:temp HandItem set from entity @s Inventory[{{Slot:0b}}]",
                    f"item replace entity @s weapon.mainhand with air",
                    f"function {ability_function}",
                    f"advancement revoke @s only {ability_name}",
                    f"data modify entity @s Inventory[{{Slot:0b}}] set from storage beetsmith:temp HandItem",
                ])
            )
        ]
        self._special_required_files.extend(files)

    @behavior
    def trim(self, pattern: str, material: str):
        ...
        self.components.trim = {
            "pattern": resourceLocation(pattern),
            "material": resourceLocation(material)
        }

    @behavior
    def weapon(self, *, attack_damage: float, attack_speed: float, can_sweep: bool, disable_blocking: float = 0, item_damage_per_attack: int = 1):
        """Adds weapon behavior to the custom item.

        #### Parameters:
            - attack_damage (int): Amount of damage dealt to entities on attack
            - attack_speed (int): Amount of fully charged attacks the item can perform per second
            - can_sweep (bool): Whether the weapon can perform sweep attacks
            - disable_blocking (float): Number of seconds hit entity's blocking ability's are disabled when hitting while it was blocking
            - item_damage_per_attack (int): Amount of durability removed when performing an attack
        """        
        self.add_attribute_modifier(attribute="minecraft:attack_damage",
                                value=attack_damage - 1,
                                slot="mainhand",
                                operation="add_value",
                                id="base_attack_damage"
                                )
        self.add_attribute_modifier(attribute="minecraft:attack_speed",
                                value=attack_speed - 4,
                                slot="mainhand",
                                operation="add_value",
                                id="base_attack_speed")
        self.components.weapon = {
            "item_damage_per_attack": item_damage_per_attack,
            "disable_blocking_for_seconds": disable_blocking
            }
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
        
        # Remove components to remove
        for component in self.removed_components:
            components[f"!{component}"] = {}
      
        return components
    
    # Delete sometime?
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
    def required_files(self) -> list[tuple[str, beet.TextFile]]:
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
            files.append((tag, beet.ItemTag(tag_data)))

        # Explicitely needed files
        files.extend(self._special_required_files)

        return files
    
    @log_duplicates
    def implement(self, datapack: beet.DataPack, /) -> None:
        """
        Implement the custom item into a beet datapack
        """
        if "right_click_ability" in self._applied_behaviours and "consumable" in self._applied_behaviours:
            warnings.warn(f"The custom item '{self.id}' has two different right-clik-behaviours (consumption and ability) which will lead to incompatibilities")

        pack_format = datapack.pack_format
        if pack_format != __minecraft_data_version__:
            warnings.warn(f"The datapack does not have the main pack format {__minecraft_data_version__}! Some content may not be loaded by Minecraft!", category=UserWarning)

        # Loottable
        datapack[self.id.replace(":", ":item/", 1)] = self.loot_table

        # Required Files
        for file in self.required_files:
            
            match file[1]:
                case beet.FunctionTag:
                    datapack.function_tags.setdefault(file[0]).merge(file[1]) # Can either merge or create function tags
            
                case beet.Function:
                    datapack.functions.setdefault(file[0]).append(file[1]) # Can either merge or create functions
                
                case _:
                    datapack[file[0]] = file[1]

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                   ArmorSet                                    │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

@dataclass
class ArmorSet:
    """Class representing a custom armor set.
    """

    id_format: InitVar[str]
    name_format: InitVar[str]
    nouns: InitVar[tuple[str, str, str, str]] = ("Helmet", "Chestplate", "Leggings", "Boots")
    trimable: InitVar[bool] = False

    items:                  list[CustomItem]    = field(init=False)
    _applied_behaviours:    list[str]           = field(init=False, default_factory=list)

    def __post_init__(self):
        ids = [resourceLocation(self.id_format.format(noun=noun).lower()) for noun in self.nouns]
        names = [self.name_format.format(noun=noun) for noun in self.nouns]

        self.items = [
            CustomItem(ids[0], names[0], "minecraft:chainmail_helmet"),
            CustomItem(ids[1], names[1], "minecraft:chainmail_chestplate"),
            CustomItem(ids[2], names[2], "minecraft:chainmail_leggings"),
            CustomItem(ids[3], names[3], "minecraft:chainmail_boots"),
        ]

        for i, item in enumerate(self.items):
            item.equippable(
                slot=armor_slots[i],
                asset="minecraft:chainmail"
            )
            if self.trimable:
                item.item = be_trimmable_ids[i]

    @property
    def helmet(self) -> CustomItem:
        return self.items[0]

    @property
    def chestplate(self) -> CustomItem:
        return self.items[1]

    @property
    def leggings(self) -> CustomItem:
        return self.items[2]

    @property
    def boots(self) -> CustomItem:
        return self.items[3]
    
    # ╭────────────────────────────────────────────────────────────╮
    # │                          Behaviour                         │ 
    # ╰────────────────────────────────────────────────────────────╯

    @behavior
    def damagable(self, *, durability: int | tuple[int, int, int, int], break_sound: str = "minecraft:entity.item.break", repair_materials: list[str] = [], additional_repair_cost: int = 0):
        ...
        for i, item in enumerate(self.items):
            if isinstance(durability, int):
                durability = armor_durability(chestplate=durability)
            else:
                durability = durability

            item.damagable(durability=durability[i], break_sound=break_sound, repair_materials=repair_materials, additional_repair_cost=additional_repair_cost)
    
    @behavior
    def enchantable(self, enchantability: int, enchantable_tag: str):
        ...
        for item in self.items:
            item.enchantable(enchantability, enchantable_tag)

    @behavior
    def full_set_ability(self, function: str):
        ...

    @behavior
    def material(self, *, model_asset: str, trim_pattern: str = None, trim_material: str = None, color: int = None, helmet_texture: str = None, equip_sound: str = "item.armor.equip_generic"):
        ...
        for i, item in enumerate(self.items):
            item.components.equippable["asset_id"] = resourceLocation(model_asset)
            item.components.equippable["equip_sound"] = resourceLocation(equip_sound)
            item.trim(trim_pattern, trim_material)
            item.components.dyed_color = color
        
        if helmet_texture:
            self.helmet.components.profile = {"properties": [{"name": "texture", "value": helmet_texture}]}
            self.helmet.components.item_model = "minecraft:player_head"

    @behavior
    def protection(self, armor: tuple[float, float, float, float], toughness: tuple[float, float, float, float] = None):
        ...
        for i, item in enumerate(self.items):
            item.add_attribute_modifier("minecraft:armor", armor_slots[i], armor[i], "add_value")
            if toughness:
                item.add_attribute_modifier("minecraft:armor_toughness", armor_slots[i], toughness[i], "add_value")

    # ╭────────────────────────────────────────────────────────────╮
    # │                        Implementation                      │ 
    # ╰────────────────────────────────────────────────────────────╯

    def implement(self, datapack: beet.DataPack, /):
        ...
        for item in self.items:
            item.implement(datapack=datapack)