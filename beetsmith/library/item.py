# https://minecraft.wiki/w/Java_Edition_hardcoded_item_properties#

from __future__ import annotations
import beet
import uuid
import warnings
from typing import Literal
from dataclasses import dataclass, field, InitVar
from beetsmith.core.text_components import normalize
from beetsmith.core.resourcelocations import ensureNoSpecialRL, ensureTagLikeRL, ensureNoTagPathRL
from beetsmith.core.compat import watch_out_for_duplicates, behavior
from beetsmith.library.components import ItemComponents, REMOVED

__minecraft_game_version__ = "1.21.9"
__minecraft_data_version__ = 88
technical_namespace = "beetsmith"
generated_file_pattern = "{technical_namespace}:{namespace}/{thing}/{id}"

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                  CustomItem                                   │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

@dataclass
class CustomItem:
    """Class representing a custom item.

    Parameter
    ----------
    id : str
        Resource location that will be used internally for the item instance
    name : str | dict | list
        Item name as a text component
    model : str
        Resource location of a model definition
    texture : str
        base64 encoded texture that will be used for the item if it has the `minecraft:player_head` model
    
    """
    id:                         str
    name:                       InitVar[str | dict | list]
    model:                      InitVar[str]
    texture:                    InitVar[str] = None

    item:                       str                             = field(init=False, default="minecraft:music_disc_11")
    components:                 ItemComponents                  = field(init=False, default_factory=ItemComponents.empty)
    required_tags:              list[str]                       = field(init=False, default_factory=list)
    _applied_behaviours:        list[str]                       = field(init=False, default_factory=list)
    _special_required_files:    list[tuple[str, beet.TextFile]] = field(init=False, default_factory=list)
    "Don't use this. Use `.required_files()` instead."

    def __post_init__(self, name, model, texture):
        self.id = ensureNoSpecialRL(self.id)
        self.components.custom_data = {"id": self.id}
        self.components.item_name = normalize(name)[0]
        self.components.item_model = ensureNoSpecialRL(model)
        if texture is not None:
            self.components.profile = {
                "properties": [{"name": "texture", "value": texture}]
            }
        self.components.unbreakable = {}
        self.components.max_stack_size = 64
        self.components.jukebox_playable = REMOVED

    def __str__(self) -> str:
        return f"<CustomItem '{self.id}' ('{self.item}' with {len(self.components.asDict())} components and {len(self._required_files())} additional files needed)>"
    
    @property
    def _id_namespace(self) -> str: return self.id.split(":")[0]
    @property
    def _id_short(self)     -> str: return self.id.split(":")[1]

    # ╭────────────────────────────────────────────────────────────╮
    # │                          Behaviors                         │ 
    # ╰────────────────────────────────────────────────────────────╯

    @behavior
    def add_attribute_modifier(
        self, *,
        attribute: str,
        slot: Literal["any", "hand", "armor", "mainhand", "offhand", "head", "chest", "legs", "feet", "body"],
        value: float, operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"],
        id: str = uuid.UUID
        ) -> None:
        """Adds a attribute modifier to the custom item.

        Parameters
        ------------
        attribute : str
            Name of the modified attribute [[Wiki](https://minecraft.wiki/w/Attribute#Attributes)]
        slot : str
            Slot where the modifier takes action
        value : float
            Amount or factor the attribute is modified with
        operation : `"add_value"` | `"add_multiplied_base"` | `"add_multiplied_total"`
            How the value is to be applied [[Wiki](https://minecraft.wiki/w/Attribute#Modifiers)]
        id : str
            Identifier of the modifier<br>
            Modifiers with the same identifier will overwrite each other<br>
            Some behaviours require specific identifiers [[Wiki](https://minecraft.wiki/w/Attribute#Vanilla_modifiers)]
        """
        if id is uuid.UUID:
            id = str(uuid.uuid4())
        self.components.attribute_modifiers = self.components.attribute_modifiers or []
        self.components.attribute_modifiers.append({
            "id": id,
            "amount": value,
            "type": attribute,
            "operation": operation,
            "slot": slot
        })

    @behavior(warn_for_incompatibility=["right_click_ability"])
    def consumable(
        self, *,
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
        function: str = None
        ) -> None:
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
            "sound": ensureNoSpecialRL(sound),
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
            ability_function = ensureNoTagPathRL(function)
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
        self.components.unbreakable = REMOVED
        self.components.break_sound = ensureNoSpecialRL(break_sound)
        self.components.damage = 0
        self.components.max_damage = durability
        self.components.repairable = {"items": [ensureTagLikeRL(material) for material in repair_materials]}
        self.components.repair_cost = additional_repair_cost
        self.components.weapon = self.components.weapon or {} # Needed for items like player heads to take damage on hit
        self.components.max_stack_size = 1

    @behavior
    def enchantable(self, enchantability: int, enchantable_tags: list[str]):
        """Adds enchantability behavior to the custom item.

        #### Parameters:
            - enchantability (int): How high the quality of enchantments is when enchanting (diamond armor has 10, gold armor has 25)
            - enchantable_tag (str): Tag that specifies what enchantments the item can get [[Examples](https://mcasset.cloud/1.21.5/data/minecraft/tags/item/enchantable)]
                - No leading `#` required since this is not a tag refference 
                - Vanilla tags begin with `enchantable/` and are `armor`, `bow`, `chest_armor`, `crossbow`, `durability`, `equippable`, `fire_aspect`, `fishing`, `foot_armor`, `head_armor`, `leg_armor`, `mace`, `mining`, `mining_loot`, `sharp_weapon`, `sword`, `trident` and `weapon`
        """
        self.components.enchantable = {"value": enchantability}
        self.required_tags.extend([ensureNoTagPathRL(tag) for tag in enchantable_tags]) # Needs to include enchantable/
    
    @behavior
    def damage_resistance(self, damage_types: list[str]) -> None:
        """Sets which damage types the custom item (as item entity or as equippable when the wearer takes damage) is immune to.

        #### Parameters
            - damage_types (list[str]): A list of damage type tags (without leading `#`) [[Wiki](https://minecraft.wiki/w/Damage_type_tag_(Java_Edition)#List_of_tags)]
        
        """
        if len(damage_types) > 1:
            tag_data = {"values": [f"#{ensureNoTagPathRL(damage_type)}" for damage_type in damage_types]}
            self._special_required_files.append((self.id, beet.DamageTypeTag(tag_data)))
            self.components.damage_resistant = {"types": f"#{self.id}"}
        else:
            self.components.damage_resistant = {"types": f"#{damage_types[0]}"}

    @behavior
    def equippable(
        self, *,
        slot: Literal["head", "chest", "legs", "feet", "body"],
        asset: str,
        equip_sound: str = "minecraft:item.armor.equip_generic",
        dispensable: bool = True,
        swappable: bool = True,
        damage_on_hurt: bool = True,
        equip_on_interaction: bool = False,
        color: int = None,
        glider: bool = False
        ) -> None:
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
            "asset_id": ensureNoSpecialRL(asset),
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
        self.components.lore = normalize(textcomponent)

    @behavior
    def rarity(self, rarity: Literal["common", "uncommon", "rare", "epic"]):
        "Sets the custom items rarity."
        if rarity in ["common", "uncommon", "rare", "epic"]:
            self.components.rarity = rarity
        else:
            raise ValueError("Rarity has to be one of 'common', 'uncommon', 'rare' or 'epic'")
    
    @behavior(warn_for_incompatibility=["consumable"])
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
        self.components.use_effects = {"can_sprint": True, "speed_multiplier": 1.0}
        
        self.components.instrument = {"range": 10, "description": normalize(description), "sound_event": "minecraft:intentionally_empty", "use_duration": 0.001}
    
        ability_name = generated_file_pattern.format(technical_namespace=technical_namespace, namespace=self._id_namespace, thing="ability", id=self._id_short) # e.g. 'customitemlib:lategame/ability/hunter_sword'
        ability_function = ensureNoTagPathRL(function)

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
                    f"data modify storage {technical_namespace}:temp HandItem set from entity @s Inventory[{{Slot:0b}}]",
                    f"item replace entity @s weapon.mainhand with air",
                    f"function {ability_function}",
                    f"advancement revoke @s only {ability_name}",
                    f"data modify entity @s Inventory[{{Slot:0b}}] set from storage {technical_namespace}:temp HandItem",
                ])
            )
        ]
        self._special_required_files.extend(files)

    @behavior
    def trim(self, pattern: str, material: str):
        ...
        self.components.trim = {
            "pattern": ensureNoSpecialRL(pattern),
            "material": ensureNoSpecialRL(material)
        }

    @behavior
    def weapon(
        self, *,
        attack_damage: float,
        attack_speed: float,
        can_sweep: bool,
        disable_blocking: float = 0,
        item_damage_per_attack: int = 1
        ) -> None:
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
    
    def asLootTablePoolEntry(self) -> dict:
        """Returns a dict, like it can be used as an item in `pools/*/entries` in a loot table definition.

        Note that, depending on the application, other functions (`·.asLootTableEntry["functions"]`) or conditions (`·.asLootTableEntry["conditions"]`) may need to be set.<br>
        This must then be done separately. Otherwise, the entire loot table can be written by hand and (`·.components.asDict()`) can be used for the components.
        """
        return {
          "type": "minecraft:item",
          "name": self.item,
          "functions": [
            {
              "function": "minecraft:set_components",
              "components": self.components.asDict()
            }
          ]
        }
    
    def asRecipeResult(self, amount: int = 1) -> dict:
        """Returns a dict, like it can be used as the value of `result` in a recipe definition.
        """
        return {
            "id": self.item,
            "components": self.components.asDict(),
            "count": amount
        }

    def _required_files(self) -> list[tuple[str, beet.TextFile]]:
        """
        Generates a list of 2-tuples whereby the first is the resourcelocation of the file and the second is a beet TextFile
        """
        files = []

        # Tags
        files.extend([
            (tag, beet.ItemTag({"replace": False, "values": [self.item]}))
            for tag in self.required_tags
        ])

        # Explicitely needed files
        files.extend(self._special_required_files)

        return files
    
    @watch_out_for_duplicates
    def implement(self, datapack: beet.DataPack, /) -> None:
        """
        Implement the custom item into a beet datapack
        """

        pack_format = datapack.pack_format
        if pack_format != __minecraft_data_version__:
            warnings.warn(f"The datapack does not match the beetsmith pack format {__minecraft_data_version__}! Some content may not be loaded by Minecraft!", category=UserWarning)

        # Loottable
        datapack[f"{self._id_namespace}:item/{self._id_short}"] = beet.LootTable(
            {
                "pools": [{
                    "rolls": 1,
                    "entries": [
                        self.asLootTablePoolEntry()
                    ]
                }]
            }
        )

        # Required Files
        for file in self._required_files():
            
            match file[1]:
                case beet.FunctionTag:
                    datapack.function_tags.setdefault(file[0]).merge(file[1]) # Can either merge or create function tags
            
                case beet.Function:
                    datapack.functions.setdefault(file[0]).append(file[1]) # Can either merge or create functions
                
                case _:
                    datapack[file[0]] = file[1]