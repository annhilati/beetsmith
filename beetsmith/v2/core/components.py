# https://minecraft.wiki/w/Data_component_format#List_of_components
# https://misode.github.io/changelog?tags=component

from dataclasses import dataclass, field, fields
from beetsmith.v2.core.resourcelocations import ResourceLocationChecker

class RemovedComponentState(object):
    def __str__(self) -> str:
        return "REMOVED"

REMOVED = RemovedComponentState()
"Constant denoting that an items component is removed"
ValidValueInComponent = list["ValidValueInComponent"] | dict[str, "ValidValueInComponent"] | int | float | str
ValidComponentValue   = None | RemovedComponentState | ValidValueInComponent

componentQueryValidator = ResourceLocationChecker(allow_tag=False, allow_negation=False)
"No negation"

@dataclass
class ItemComponents():
    """Class representing a Minecraft item's components.

    You really shouldn't use the constructor of this class.<br>
    Use `.fromDict()`, `.fromVanillaItem()` or `.empty()` instead.

    Only some vanilla components are accessible through attributes. Item setting and getting can be used instead.

    To remove a component, set it's value to `REMOVED`. It can be imported from this same module.

    Supports
    ---------
    - `·[...]`
    - `·[...] = ...`
    - `str(·)`
    """
    attribute_modifiers:         list[dict]          = None
    block_attacks:               dict                = None
    break_sound:                 str                 = None
    consumable:                  dict                = None
    custom_data:                 dict                = None
    damage:                      int                 = None
    damage_resistant:            dict                = None
    death_protection:            dict                = None
    dyed_color:                  int | list          = None
    enchantable:                 dict                = None
    enchantment_glint_override:  bool                = None
    enchantments:                dict                = None
    equippable:                  dict                = None
    food:                        dict                = None
    glider:                      dict                = None
    instrument:                  dict                = None
    item_model:                  str                 = None
    item_name:                   str | dict | list   = None
    jukebox_playable:            str                 = None
    lore:                        str | dict | list   = None
    max_damage:                  int                 = None
    max_stack_size:              int                 = None
    profile:                     dict                = None
    potion_content:              dict                = None
    rarity:                      str                 = None
    repairable:                  dict                = None
    repair_cost:                 int                 = None
    tool:                        dict                = None
    tooltip_display:             dict                = None
    trim:                        dict                = None
    unbreakable:                 dict                = None
    use_cooldown:                dict                = None
    use_remainder:               dict                = None
    weapon:                      dict                = None

    _other_components:           dict[str, ValidComponentValue] = field(default_factory=dict)

    @property
    def _vanilla_components(self) -> dict[str, ValidComponentValue]:
        return {
            field.name: getattr(self, field.name)
            for field
            in fields(self)
            if field.name not in ["_other_components"]}

    def _set_component(self, component: str, value: ValidComponentValue) -> None:
        componentQueryValidator(component)
        id = componentQueryValidator.id(component)
        
        if id in self._vanilla_components:
            setattr(self, id, value)
        else:
            self._other_components[component] = value

    def _get_component(self, component: str) -> ValidComponentValue:
        return (
            getattr(self, component.split(":")[-1])
            if component in self._vanilla_components
            else self._other_components.get(component)
        )
    
    @classmethod
    def empty(cls):
        return cls()
     
    @classmethod
    def fromDict(cls, data: dict[str, ValidValueInComponent], /):
        """Create an ItemComponents instance from a dictionary.
        
        The type of dictionary required is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        instance: ItemComponents = cls()

        for component, value in data.items():
            if component.startswith("!"):
                value = REMOVED
            instance._set_component(component, value)
        return instance
    
    @classmethod
    def fromVanillaItem(cls, id: str, /):
        """Create an ItemComponents instance from the data of a vanilla item.
        
        This will issue a HTTP request (~800 kB).

        If no data is found for the specified item id, an empty ItemComponents instance is returned.
        """
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
        
        The type of dictionary produced is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        out = {}

        for component, value in self._vanilla_components.items():
            if value is not REMOVED and value is not None:
                out["minecraft:" + component] = value
            elif value is REMOVED and value is not None:
                out["!minecraft:" + component] = {}

        for component, value in self._other_components.items():
            if value is not REMOVED and value is not None:
                out[component] = value
            elif value is REMOVED and value is not None:
                out["!" + component] = {}
        
        return out
    
    def __str__(self) -> str:
        return str(self.asDict())

    def __getitem__(self, query: str) -> ValidComponentValue:
        return self._get_component(component=query)

    def __setitem__(self, query: str, value: ValidComponentValue) -> None:
        self._set_component(component=query, value=value)