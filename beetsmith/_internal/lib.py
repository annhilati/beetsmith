import re

def armor_durability(*, helmet: int = None, chestplate: int = None, leggings: int = None, boots: int = None):
    
    if len([arg for arg in [helmet, chestplate, leggings, boots] if type(arg) != None]) in [0, 2, 3]:
        raise ValueError("Please state one durability")
    
    # obere Liste ist der zu berechnende Slot, untere Liste der bekannte Slot
    factors = [
        [1, 0.6875, 0.7333, 0.8412],
        [1.4546, 1, 1.0667, 1.2284],
        [1.3637, 0.9375, 1, 1.1505],
        [1.1887, 0.8152, 0.8690, 1]
    ]

    durabilities = [helmet, chestplate, leggings, boots]

    for slot, durability in enumerate(durabilities):
        if durability is None:
            for other_slot, other_durability in enumerate(durabilities):
                if other_durability is not None:
                    durabilities[slot] = round(durabilities[other_slot] * factors[slot][other_slot])
    
    return durabilities

def refer(function, /):
    """
    Calls another function with the arguments passed into the decorated function
    #### Usage
    ```
    @refer(lib.this_function)
    def new_function():
        ...
    ```
    """
    if isinstance(function, classmethod) or isinstance(function, staticmethod):
        function = function.__func__

    def decorator(method):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator

def extract_key(e: Exception):
    msg = str(e)
    if "got an unexpected keyword argument" in msg:
        cause = "unexpected"
        match = re.search(r"got an unexpected keyword argument '(\w+)'", msg)
        if match:
            invalid_kwarg = match.group(1)

    elif "missing 1 required positional argument" in msg:
        cause = "missing"
        match = re.search(r"missing 1 required positional argument: '(\w+)'", msg)
        if match:
            invalid_kwarg = match.group(1)

    else:
        raise Exception("extract_key() doesn't know this Exception")

    return (cause, invalid_kwarg)