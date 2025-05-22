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
