def version(doc_note: str):
    def decorator(cls):
        # Klasse: Docstring erweitern
        if cls.__doc__:
            cls.__doc__ += f"\n\n{doc_note}"
        else:
            cls.__doc__ = doc_note

        # __init__: Docstring erweitern (falls vorhanden)
        init = getattr(cls, '__init__', None)
        if init and init.__doc__:
            init.__doc__ += f"\n\n{doc_note}"
        elif init:
            init.__doc__ = doc_note

        return cls
    return decorator

def ensureResourceLocation(str: str) -> str:
    for char in str.lower():
        if char not in "abcdefghijklmnopqrstuvwxyz_/:":
            raise ValueError(f"{str} is not a valid resource location")
        
    if str.startswith(":") or str.endswith(":"):
        raise ValueError(f"{str} is not a valid resource location")
    
    if str.count(":") == 1:
        return str
    elif str.count(":") == 0:
        return f"minecraft:{str}"
    else:
        raise ValueError(f"{str} is not a valid resource location")