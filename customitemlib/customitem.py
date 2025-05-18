import json
from pydantic import BaseModel

TYPE_FOR_MATERIAL = "minecraft:music_disc_11"

class ItemComponents(BaseModel):
    """
    Current version: 1.21.5
    """
    item_name: str | dict = None
    item_model: str = None
    jukebox_playable: str = None
    profile: dict = None

class CustomItem():
    def __init__(self, name: str | dict, model: str, type: str = "material"):
        """
        Creates a data model of a custom item

        #### Arguments
            - name (str | dict): The items name
            - model (str): The items model. Refers to a asseted model
            - type (str): A predefined item type. One of `material`
        
        #### Settings
            - headtexture (str): The items texture as encoded base64, if it has the player head model
        """
        
        #self.components_overwrite = {}

        self.name = name
        self.model = model
        self.headtexture: str = None

        if type in ["material"]:
            self.type = type
        else:
            raise ValueError
    
    @property
    def components(self) -> dict:

        # ╭────────────────────────────────────────────────────────────╮
        # │                      Set ItemComponents                    │ 
        # ╰────────────────────────────────────────────────────────────╯
        components = ItemComponents()
        components.item_name = self.name
        components.item_model = self.model

        if self.headtexture:
            components.profile = {"properties": [{"name": "texture", "value": self.headtexture}]}

        # ╭────────────────────────────────────────────────────────────╮
        # │               Build dict from ItemComponents               │ 
        # ╰────────────────────────────────────────────────────────────╯
        component_stack = components.model_dump()
        
        # Remove components unset in the ItemComponents abstraction
        unset_components = [key for key, value in components.model_dump().items() if value is None]
        for component in unset_components:
            component_stack.pop(component)

        # Remove components
        removed_components = []

        match self.type:
            case "material":
                removed_components.append("jukebox_playable")
            case _:
                raise ValueError
        
        for component in removed_components:
            component_stack[f"!{component}"] = {}
        
        return component_stack
    
    def componentsJSON(self, indent: int = 4) -> str:
        return json.dumps(self.components, indent=indent, ensure_ascii=False)
    
    @property
    def item(self) -> str:
        
        match self.type:
            case "material":
                self.item = TYPE_FOR_MATERIAL
            case _:
                raise ValueError