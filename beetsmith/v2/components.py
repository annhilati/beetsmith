# https://minecraft.wiki/w/Data_component_format#List_of_components
# https://misode.github.io/changelog?tags=component

from dataclasses import dataclass, field, fields
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from v2.resourcelocations import ResourceLocationChecker

class RemovedComponentState(object):
    def __str__(self) -> str:
        return "REMOVED"

REMOVED = RemovedComponentState()
"Constant denoting that an item component is removed"
ValidValueInComponent = list["ValidValueInComponent"] | dict[str, "ValidValueInComponent"] | int | float | str
ValidComponentValue   = None | RemovedComponentState | ValidValueInComponent

componentValidator = ResourceLocationChecker(allow_tag=False, allow_negation=False)
"No negation"

@dataclass
class ItemComponents():
    """Class representing a Minecraft item's components.

    You really shouldn't use the constructor of this class. Use `.fromDict()` or `.fromVanillaItem()` instead.

    Only some vanilla components are accessible through attributes. Item setting and getting can be used instead.

    Supports
    ---------
    - `str(·)`
    - `·[...]`
    - `·[...] = ...`
    """
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

    _other_components:              dict[str, ValidComponentValue] = field(default_factory=dict)


    @property
    def _vanillaFields(self) -> list[str]:
        return {f.name for f in fields(self) if f.name != "_other_components"}

    def _set_component(self, component: str, value: ValidComponentValue) -> None:
        
        componentValidator(component)
        id = componentValidator.id(component)
        
        if id in self._vanillaFields:
            setattr(self, id, value)
        else:
            self._other_components[component] = value

    def _get_component(self, component: str) -> ValidComponentValue:
        return (
            getattr(self, component.split(":")[-1])
            if component in self._vanillaFields
            else self._other_components.get(component)
        )
    
    @classmethod
    def fromDict(cls, data: dict[str, ValidValueInComponent], /):
        instance: ItemComponents = cls()

        for component, value in data.items():
            if component.startswith("!"):
                value = REMOVED
            instance._set_component(component, value)
        return instance
    
    @classmethod
    def fromVanillaItem(cls, id: str, /):
        "Requires the if of a vanilla item"
        import requests

        query = id.split(":")[-1]
        url = "https://raw.githubusercontent.com/misode/mcmeta/summary/item_components/data.json"
        res = requests.get(url)
        res.raise_for_status()
        data: dict[str, dict] = res.json()

        if query not in data:
            return cls()
        
        return cls.fromDict(data[query])

    def asDict(self) -> dict[str, ValidValueInComponent]:
        """Return the item components as a dictionary.
        
        The type of dictionary produced here is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """

        main_fields = {
            f"minecraft:{field}": getattr(self, field)
            for field in self._vanillaFields
            if getattr(self, field) is not None
            and getattr(self, field) is not REMOVED
        }
        main_fields.update({
            f"!minecraft:{field}": {}
            for field in self._vanillaFields
            if getattr(self, field) is REMOVED
        })
        other_fields = {
            key: value
            for key, value in getattr(self, "_other_components", {}).items()
            if value is not REMOVED
        }
        other_fields.update({
            f"!{key}": {}
            for key, value in getattr(self, "_other_components", {}).items()
            if value is REMOVED
        })

        return {
            **main_fields,
            **other_fields
        }
    
    def __str__(self) -> str:
        return str(self.asDict())

    def __getitem__(self, query: str) -> ValidComponentValue:
        return self._get_component(component=query)

    def __setitem__(self, query: str, value: ValidComponentValue) -> None:
        self._set_component(component=query, value=value)

# components = ItemComponents.fromDict({
#     "minecraft:equippable": {"lol"},
#     "weapon": REMOVED,
#     "random:data": ["wow", "!"]
# })
components = ItemComponents.fromVanillaItem("elytra")
components._set_component("player", {"test"})
print(components.asDict())