import yaml
import pathlib

# def load_item_from_yaml(file: str | pathlib.Path):
#     # Creates a CustomItem object from a yaml file

#     with open(file, 'r') as f:
#         data: dict = yaml.safe_load(f)

#     item = CustomItem(id=data["id"], name=data["name"], model=data["model"], texture=data.get("texture"))

#     for template in data["templates"]:
#         method_name, args = template.items()
#         method = getattr(item, method_name, None)
#         if method is None or not callable(method):
#             raise ValueError(f"'{method_name}' is not a valid template")
#         if not isinstance(args, dict):
#             raise ValueError(f"Arguments for '{method_name}' have to be in a key-value format")
#         method(**args)

#     # for method_name, args in {k: v for k, v in data[].items() if k not in ["id", "name", "model", "texture"]}.items():
#     #     method = getattr(item, method_name, None)
#     #     if method is None or not callable(method):
#     #         raise ValueError(f"'{method_name}' is not a valid template")
#     #     if not isinstance(args, dict):
#     #         raise ValueError(f"Arguments for '{method_name}' have to be in a key-value format")
#     #     method(**args)

#     return item