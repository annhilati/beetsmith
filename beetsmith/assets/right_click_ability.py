from ..typewriter.templates import *

trigger_advancement: Template[dict] = Template(
    {
        "criteria": {
            "use_item": {
                "trigger": "minecraft:using_item",
                "conditions": {
                    "item": {
                        "predicates": {
                            "minecraft:custom_data": {
                                    "id": Placeholder("id", str, identity)
                            }
                        }
                    }
                }
            }
        },
        "rewards": {
            "function": Placeholder("ability_function", str, identity)
        }
    }
)

controll_function: Template[list[str]] = [
    "data modify storage {storage} HandItem set from entity @s Inventory[{{Slot:0b}}]"
    "item replace entity @s weapon.mainhand with air"
    "function {ability_function}"
    "advancement revoke @s only {trigger_advancement}"
    "data modify entity @s Inventory[{{Slot:0b}}] set from storage {storage} HandItem"
]