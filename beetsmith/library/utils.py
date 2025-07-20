def armor_durability(*, helmet: int = None, chestplate: int = None, leggings: int = None, boots: int = None) -> tuple[int, int, int, int]:
    
    if len([arg for arg in [helmet, chestplate, leggings, boots] if type(arg) != None]) in [0, 2, 3]:
        raise ValueError("Exactly one known durability needed")
    
    # erster Index ist der zu berechnende Slot, zweiter Index der bekannte Slot
    factors = [
        [1, 0.6875, 0.7333, 0.8412],
        [1.4546, 1, 1.0667, 1.2284],
        [1.3637, 0.9375, 1, 1.1505],
        [1.1887, 0.8152, 0.8690, 1]
    ]

    durabilities = (helmet, chestplate, leggings, boots)

    for slot, durability in enumerate(durabilities):
        if durability is None:
            for other_slot, other_durability in enumerate(durabilities):
                if other_durability is not None:
                    durabilities[slot] = round(durabilities[other_slot] * factors[slot][other_slot])
    
    return durabilities