from beetsmith.v2.core.components import ItemComponents
from beetsmith.v2.core.resourcelocations import ResourceLocationChecker
from beetsmith.v2.library.customitem import Item

item = Item("test:item", "Testitem", "minecraft:diamond")
print(item)
print(item.asLootTablePoolEntry())