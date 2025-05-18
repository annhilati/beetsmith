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

class CustomItem():
    def __init__(self, name: str | dict, model: str, type: str = "material"):
        
        #self.components_overwrite = {}

        self.item: str = None
        "Technical Minecraft item as namespaced id"

        # Meta
        self.name = name
        self.model = model


        self.removed_components = []

        match type:
            case "material":
                self.item = TYPE_FOR_MATERIAL
                self.removed_components.append("jukebox_playable")
            case _:
                raise ValueError
    
    @property
    def components(self) -> dict:

        # ItemComponent Builder
        components = ItemComponents()
        components.item_name = self.name
        components.item_model = self.model

        # Component Stack Builder
        component_stack = components.model_dump()
        
        unset_components = [key for key, value in components.model_dump().items() if value is None]
        for component in unset_components:
            component_stack.pop(component)
        
        for component in self.removed_components:
            component_stack[f"!{component}"] = {}
        
        return component_stack
    
    def componentsJSON(self, indent: int = 4) -> str:
        return json.dumps(self.components, indent=indent, ensure_ascii=False)