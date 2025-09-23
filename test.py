from beetsmith.v2.components import ItemComponents
from beetsmith.v2.resourcelocations import ResourceLocationChecker

data = ItemComponents.fromVanillaItem("diamond_sword")

print(data.asDict())