import json
from pydantic import BaseModel

class ItemComponents(BaseModel):
    """
    Current version: 1.21.5
    """
    attribute_modifier: list[dict] = None
    damage: int = None
    item_model: str = None
    item_name: str | dict = None
    jukebox_playable: str = None
    max_damage: int = None
    profile: dict = None
    tool: dict = None
    weapon: dict = None

class CustomItem():
    "Data model representing a custom item"
    def __init__(self, name: str | dict, model: str):
        """
        Data model representing a custom item

        #### Parameters
            - name (str | dict): Name of the item as a plain string or text component as a dict
            - model (str): Asset name of the items model

        #### Modifier
            Can be set by asigning a value to these properties
            - headtexture (str): The items texture if it has a player head model as encoded base64
            - weapon
        """

        self.item = "minecraft:music_disc_11"
        self.removed_components = ["jukebox_playable"]
        self.components = ItemComponents()
        self.components.item_name = name
        self.components.item_model = model

    @property
    def headtexture(self):
        if self.components.profile:
            return self.components.profile["properties"][0]["value"]
        return None
    
    @headtexture.setter
    def headtexture(self, headtexture: str):
        self.components.profile = {"properties": [{"name": "texture", "value": headtexture}]}
    
    @property
    def item(self) -> str:
        return self._item
    
    @item.setter
    def item(self, item: str):
        self._item = item
    
    def set_weapon(self, max_damage: int, item_damage_per_attack: int = 1):
        self.components.weapon = {"item_damage_per_attack": item_damage_per_attack}
        self.components.max_damage = max_damage
        self.components.damage = 0
        self.components.tool = {"rules": [], "can_destroy_blocks_in_creative": False}
    
    
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
    
    def componentsJSON(self, indent: int = 4) -> str:
        return json.dumps(dict(self), indent=indent, ensure_ascii=False)