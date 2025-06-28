class Template:
    def __init__(self):
        ...

# def ersetzen_template(obj: Any, mapping: dict[str, Any]) -> Any:
#     if isinstance(obj, str):
#         return string.Template(obj).safe_substitute(mapping)
#     elif isinstance(obj, list):
#         return [ersetzen_template(e, mapping) for e in obj]
#     elif isinstance(obj, dict):
#         return {k: ersetzen_template(v, mapping) for k, v in obj.items()}
#     else:
#         return obj