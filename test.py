from beetsmith.library.components import ItemComponents
from beetsmith.library.item import CustomItem
from beetsmith.core.resourcelocations import ResourceLocationChecker

# item = Item("test:item", "Testitem", "minecraft:diamond")
# print(item)
# item.right_click_ability(description="", cooldown=5, function="chill:chill")
# item.consumable(time=1.0, animation="none", nutrition=0, saturation=0, consume_always=False, particles=False)
# item.implement(...)

cp1 = ItemComponents.fromDict({"item_model": "diamond"})
cp2 = ItemComponents.fromDict({"item_model": "netherite"})



print(cp1 | cp2)