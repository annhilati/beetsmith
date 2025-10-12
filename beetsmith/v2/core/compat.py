import beet
import warnings
import inspect, functools
from typing import Callable, cast, TypeVar

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

F = TypeVar("F", bound=Callable)

def behavior(fn: F | None = None, *, warn_for_incompatibility: list[str] | None = None) -> F:
    def decorator(inner_fn: F) -> F:
        @functools.wraps(inner_fn)
        def wrapper(self, *args, **kwargs):
            if warn_for_incompatibility:
                for incompat in warn_for_incompatibility:
                    if incompat in getattr(self, "_applied_behaviours", []):
                        warnings.warn(
                            f"The two applied behaviours '{inner_fn.__name__}' and '{incompat}' "
                            "may be incompatible or cause unexpected behavior."
                        )
            self._applied_behaviours.append(inner_fn.__name__)
            return inner_fn(self, *args, **kwargs)
        return cast(F, wrapper)

    if fn is None:
        return decorator
    return decorator(fn)
