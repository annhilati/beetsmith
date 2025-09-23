# https://minecraft.wiki/w/Data_component_format#List_of_components
# https://misode.github.io/changelog?tags=component

from dataclasses import dataclass, fields

class RemovedComponentState(object):
    def __str__(self) -> str:
        return "REMOVED"

REMOVED = RemovedComponentState()
"Constant denoting that an item component is removed"
ValidValueInComponent = list["ValidValueInComponent"] | dict[str, "ValidValueInComponent"] | int | float | str
ValidComponentValue   = None | RemovedComponentState | ValidValueInComponent

@dataclass
class ItemComponents():
    """Class representing a Minecraft item's components.

    You really shouldn't use the constructor of this class. Use `.fromDict()` or `.fromVanillaItem()` instead.

    Only some vanilla components are accesible through attributes. For components

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

    _other_components:              dict[str, ValidComponentValue] = None

    def __str__(self) -> str:
        return str(self.asDict())

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

    @classmethod
    def fromDict(cls, data: dict[str, ValidValueInComponent], /):
        """Create an ItemComponent object from a dictionary.
        
        The type of dictionary required here is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        allowedFields = {f.name for f in fields(cls)}

        main_fields = {
            component.split(":")[-1]: value
            for component, value
            in data.items()
            if component.split("minecraft:")[-1] in allowedFields
            and not component.startswith("!")
        }
        main_fields.update({
            component.split("!")[-1].split(":")[-1]: REMOVED
            for component, value
            in data.items()
            if component.split("!")[-1].split(":")[-1] in allowedFields
            and component.startswith("!")
        })
        other_fields = {
            component: value
            for component, value
            in data.items()
            if component.split("minecraft:")[-1] not in allowedFields
            and not component.startswith("!")
        }
        other_fields.update({
            component.split("!")[-1]: REMOVED
            for component, value
            in data.items()
            if component.split("!")[-1].split("minecraft:")[-1] not in allowedFields
            and component.startswith("!")
        })
        
        return cls(**{
            **{component: value for component, value in main_fields.items()},
            "_other_components": other_fields
        })

    @property
    def asDict(self) -> dict[str, ValidValueInComponent]:
        """Return the item components as a dictionary.
        
        The type of dictionary produced here is like the ones used in every JSON definition of item components like in recipes, item modifiers and loot tables,<br>
        whereby the keys are the names of the components which can have a leading `!` and their values are the components values.
        """
        allowedFields = {f.name for f in fields(self)}

        main_fields = {
            f"minecraft:{field}": getattr(self, field)
            for field in allowedFields
            if getattr(self, field) is not None
            and getattr(self, field) is not REMOVED
            and field != "_other_components"
        }
        main_fields.update({
            f"!minecraft:{field}": {}
            for field in allowedFields
            if getattr(self, field) is REMOVED
            and field != "_other_components"
        })
        other_fields = {
            key: value
            for key, value in getattr(self, "_other_components", {}).items()
            if value is not REMOVED
        }
        other_fields.update({
            f"!{key}": None
            for key, value in getattr(self, "_other_components", {}).items()
            if value is REMOVED
        })

        return {
            **main_fields,
            **other_fields
        }
    
    def __getitem__(self, query: str) -> ValidComponentValue | None:
        return (
            getattr(self, query.split(":")[-1])
            or self._other_components.get(query)
            or None
        )

    def __setitem__(self, query: str, value: ValidComponentValue) -> None:
        allowedFields = {f.name for f in fields(self)}
        if query.split(":")[-1] in allowedFields:
            setattr(self, query.split(":")[-1], value)
        else:
            self._other_components[query] = value

    # We need methods separate from the dunders here
    # def __getattr__(self, query: str) -> ValidComponentValue | None:
    #     return self.__getitem__(query=query)
    
    # def __setattr__(self, query: str, value: ValidComponentValue) -> None:
    #     return self.__setitem__(query=query, value=value)

components = ItemComponents.fromDict({
    "minecraft:equippable": {"lol"},
    "weapon": REMOVED,
    "random:data": ["wow", "!"]
})
components.tax = {"test"}
print(components.asDict)