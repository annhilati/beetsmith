import yaml
import beet
import pathlib
import warnings
from .core import CustomItem, ArmorSet

def create_from_yaml(file: str | pathlib.Path) -> CustomItem | ArmorSet:
        """
        Creates a CustomItem object from a file in a certain yaml based definition format
        """
        with open(file, 'r') as f:
            data: dict = yaml.safe_load(f)

        type = [type for type in [CustomItem, ArmorSet] if type.__name__ == data["type"]][0]

        obj = type(**{arg: value for arg, value in data.items() if arg not in ["type", "behaviour"]})


        for template in data["behaviour"]:
            method_name, args = list(template.items())[0]
            method = getattr(obj, method_name, None)
            if method is None or not callable(method):
                raise ValueError(f"'{method_name}' is not a valid behaviour for a {type(obj).__name__}")
            if not isinstance(args, dict):
                raise ValueError(f"Arguments for '{method_name}' have to be in a key-value format")
            method(**args)

        return obj

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
            item: CustomItem = create_from_yaml(file)
            item.implement(datapack)

        except Exception as e:
            warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)
