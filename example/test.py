from beetsmith import Item

item = Item(id="test", name="Test", model="minecraft:diamond")
item.weapon(attack_damage=10,
            attack_speed=10,
            can_sweep=False)

print(item)
print(item._applied_behaviours)

item = Item(id="test", name="Test", model="minecraft:diamond")

item.rarity