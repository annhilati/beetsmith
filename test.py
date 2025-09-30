from beetsmith.v2.library.components import ItemComponents
from beetsmith.v2.library.item import Item
from beetsmith.v2.core.resourcelocations import ResourceLocationChecker

item = Item("test:item", "Testitem", "minecraft:diamond")
print(item)
item.right_click_ability(description="", cooldown=5, function="chill:chill")
item.consumable(time=1.0, animation="none", nutrition=0, saturation=0, consume_always=False, particles=False)
item.implement(...)