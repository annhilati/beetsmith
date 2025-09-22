import requests
import json
from dataclasses import dataclass, asdict
from typing import Any

class RemovedComponentState(object):
    def __str__() -> str:
        return "REMOVED"

REMOVED = RemovedComponentState()
"Constant denoting that an item component is removed"

@dataclass
class ItemComponents():
    """Class representing a Minecraft item's components.
    """
    # https://minecraft.wiki/w/Data_component_format#List_of_components
    # https://misode.github.io/changelog?tags=component
    attribute_modifiers:            list[dict]          = None
    block_attacks:                  dict                = None
    break_sound:                    str                 = None
    consumable:                     dict                = None
    custom_data:                    dict                = None
    damage:                         int                 = None
    damage_resistant:               dict                = None
    death_protection:               dict                = None
    dyed_color:                     int | list          = None
    enchantable:                    dict                = None
    enchantment_glint_override:     bool                = None
    enchantments:                   dict                = None
    equippable:                     dict                = None
    food:                           dict                = None
    glider:                         dict                = None
    instrument:                     dict                = None
    item_model:                     str                 = None
    item_name:                      str | dict | list   = None
    jukebox_playable:               str                 = None
    lore:                           str | dict | list   = None
    max_damage:                     int                 = None
    max_stack_size:                 int                 = None
    profile:                        dict                = None
    potion_content:                 dict                = None
    rarity:                         str                 = None
    repairable:                     dict                = None
    repair_cost:                    int                 = None
    tool:                           dict                = None
    tooltip_display:                dict                = None
    trim:                           dict                = None
    unbreakable:                    dict                = None
    use_cooldown:                   dict                = None
    use_remainder:                  dict                = None
    weapon:                         dict                = None
    _modded_components:             dict                = None

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @classmethod
    def fromVanillaItem(cls, id: str):
        "Requires the if of a vanilla item"
        query = id.split(":")[-1]
        url = "https://raw.githubusercontent.com/misode/mcmeta/summary/item_components/data.json"
        res = requests.get(url)
        res.raise_for_status()
        data: dict[str, dict] = res.json()

        if query not in data:
            return cls()
        
        return cls.fromDict(data[query])

    @classmethod
    def fromDict(cls, data: dict[str, Any]):
        "Requires a dictionary where the keys are the names of components and the values are their values."
        components = {
            component.split(":")[-1]: value
            for component, value
            in data.items()
            if not component.startswith("!")
        }
        components.update({
            component.split(":")[-1]: REMOVED
            for component
            in data
            if component.startswith("!")
        })
        
        return cls(**components)
    
    def toDict(self) -> dict:
        _ = {
            component: value
            for component, value
            in asdict(self).items()
            if value is not REMOVED and value is not None
        }
        _.update({
            "!" + component: {}
            for component, value
            in asdict(self).items()
            if value is REMOVED
        })

        return _

print(ItemComponents.fromVanillaItem("elytra").toDict())