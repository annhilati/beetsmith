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
        
        self.components = ItemComponents()
        "Technical item component stack as pydantic modelation. For removed components see `self.removed_components` (list[str])"
        self.components.item_name = name
        self.components.item_model = model

        self.item: str = None
        "Technical Minecraft item as namespaced id"

        self.removed_components = []

        match type:
            case "material":
                self.item = TYPE_FOR_MATERIAL
                self.removed_components.append("jukebox_playable")
            case _:
                raise ValueError