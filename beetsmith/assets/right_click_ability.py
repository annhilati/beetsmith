trigger_advancement = """
{
    "criteria": {
        "use_item": {
            "trigger": "minecraft:using_item",
            "conditions": {
                "item": {
                    "predicates": {
                        "minecraft:custom_data": {
                                "id": {id}
                        }
                    }
                }
            }
        }
    },
    "rewards": {
        "function": {ability_function}
    }
}
"""

controll_function = """
data modify storage {storage} HandItem set from entity @s Inventory[{{Slot:0b}}]
item replace entity @s weapon.mainhand with air
function {ability_function}
advancement revoke @s only {trigger_advancement}
data modify entity @s Inventory[{{Slot:0b}}] set from storage {storage} HandItem
"""