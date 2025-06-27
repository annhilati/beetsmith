import beet
import yaml
import pathlib
import warnings
from .core import CustomItem

def create_from_yaml(cls, file: str | pathlib.Path):
        # Creates a CustomItem object from a yaml file

        with open(file, 'r') as f:
            data: dict = yaml.safe_load(f)

        item = CustomItem(id=data["id"], name=data["name"], model=data["model"], texture=data.get("texture"))

        for method_name, args in {k: v for k, v in data.items() if k not in ["id", "name", "model", "texture"]}.items():
            method = getattr(item, method_name, None)
            if method is None or not callable(method):
                raise ValueError(f"'{method_name}' is not a valid template")
            if not isinstance(args, dict):
                raise ValueError(f"Arguments for '{method_name}' have to be in a key-value format")
            method(**args)

        return item

def load_dir_and_implement(directory: str | pathlib.Path, datapack: beet.DataPack) -> None:
    """
    Looks for yaml files in a directory and implements all of them into a contexts datapack

    #### Parameters:
        - datapack (DataPack): A beet datapack object
        - directory (str): Directory path with desired files
    """
    directory = pathlib.Path(directory) if not isinstance(directory, pathlib.Path) else directory
    files = [filepath for filepath in directory.glob("*.yml")] + [filepath for filepath in directory.glob("*.yaml")]

    for file in files:
        try: 
            item: CustomItem = CustomItem.create_from_yaml(file)
            item.implement(datapack)

        except Exception as e:
            warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)