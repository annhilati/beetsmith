from beetsmith import CustomItem

item = CustomItem(id="test", name="Test", model="minecraft:diamond")
item.weapon(attack_damage=10,
            attack_speed=10,
            can_sweep=False)

print(item)
print(item._applied_behaviours)

item = CustomItem(id="test", name="Test", model="minecraft:diamond")