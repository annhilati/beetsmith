import re
import json
from typing import Any

resourceLocationPattern = r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)*$" # currently: never leading special symbols

def resourceLocation(str: str):
    """
    Ensures that the argument is formatted like a valid resource location and passes it on
    
    #### Valid Examaples
        - `minecraft:item`
        - `custom:tree3`
        - `justastring`

    #### Raises
        - ValueError: If str is not in a valid format
    """

    if ":" not in str:
        str = "minecraft:" + str
    
    if not re.match(resourceLocationPattern, str):
        raise ValueError(f"{str} does not match the pattern of resource loactions")
    
    return str