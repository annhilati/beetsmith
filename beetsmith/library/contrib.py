from typing import Literal
from beetsmith.core.classes import CustomItem
import beet

def shaped_recipe(result: CustomItem,
                  items: tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]],
                  category: Literal["building", "redstone", "misc", "equipment"] = "misc")-> beet.Recipe:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        pattern = []
        register = {}
        for row in items:
            pattern_row = ""
            for item in row:
                if item is None:
                    pattern_row += " "
                elif item in register:
                    pattern_row += register[item]
                else:
                    pattern_row += alphabet[len(register)]
                    register[item] = alphabet[len(register)]
            pattern.append(pattern_row)

        json = {
            "type": "minecraft:crafting_shaped",
            "category": category,
            "pattern": pattern,
            "key": {key: item for item, key in register.items()},
            "result": {
                "id": result.item,
                "components": result._components_data
            }
        }

        return beet.Recipe(json)