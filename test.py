from beetsmith.v2.core.components import ItemComponents
from beetsmith.v2.core.resourcelocations import ResourceLocationChecker
from beetsmith.v2.library.customitem import CustomItem

item = CustomItem("test:item", "Testitem", "minecraft:diamond")
print(item.components.asDict())
print(item)