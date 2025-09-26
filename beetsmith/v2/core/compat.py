import beet
import inspect
import warnings
import functools
from typing import Callable

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

def behavior(fn: Callable = None, *, warn_for_incompatability: list[str] = None):
    # Wenn direkt eine Funktion übergeben wurde -> einfacher Decorator
    if fn is not None and callable(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if warn_for_incompatability:
                for incompatability in warn_for_incompatability:
                    if incompatability in self._applied_behaviours:
                        warnings.warn(
                            f"The two applied behaviours '{fn.__name__}' and '{incompatability}' "
                            "may be incompatible or cause unexpected behavior."
                        )
            self._applied_behaviours.append(fn.__name__)
            return fn(self, *args, **kwargs)
        return wrapper

    # Sonst -> Decorator-Factory zurückgeben
    def decorator(inner_fn: Callable):
        @functools.wraps(inner_fn)
        def wrapper(self, *args, **kwargs):
            if warn_for_incompatability:
                for incompatability in warn_for_incompatability:
                    if incompatability in self._applied_behaviours:
                        warnings.warn(
                            f"The two applied behaviours '{inner_fn.__name__}' and '{incompatability}' "
                            "may be incompatible or cause unexpected behavior."
                        )
            self._applied_behaviours.append(inner_fn.__name__)
            return inner_fn(self, *args, **kwargs)
        return wrapper
    return decorator