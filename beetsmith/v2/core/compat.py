import beet
import inspect
import warnings
import functools

REGISTERED_IMPLEMENTATIONS: set[tuple[str, beet.DataPack]] = set()
"Live action value"

def watch_out_for_duplicates(func):
    "Watches implemented custom item's ids on `core.compat.REGISTERED_IMPLEMENTATIONS` and warns on duplicates."
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        id: str = getattr(self, "id", None)

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        datapack: beet.DataPack = bound.arguments.get("datapack")

        if (id, datapack) in REGISTERED_IMPLEMENTATIONS:
            warnings.warn(f"Multiple custom items with the id '{id}' were implemented")
        else:
            REGISTERED_IMPLEMENTATIONS.add((id, datapack))

        return func(*args, **kwargs)
    return wrapper