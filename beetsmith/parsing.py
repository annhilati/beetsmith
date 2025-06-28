import re
import yaml
import beet
import pathlib
import warnings
from .core import CustomItem, ArmorSet

allowed_types = [CustomItem, ArmorSet]

# Developer Note:
#   create_from_yaml shall be raising exceptions on problems,
#   but load_dir_and_implement shall only warn the user.

def create_from_yaml(file: str | pathlib.Path) -> CustomItem | ArmorSet:
        """
        Creates a CustomItem object from a file in a certain yaml based definition format
        """
        with open(file, 'r') as f:
            data: dict = yaml.safe_load(f)

        try:
            obj_type = [type for type in allowed_types if type.__name__ == data["type"]][0]
            obj = obj_type(**{param: value for param, value in data.items() if param not in ["type", "behaviour"]})
        
        except Exception as e:
            msg = str(e)
            
            if "got an unexpected keyword argument" in msg:
                match = re.search(r"got an unexpected keyword argument '(\w+)'", msg)
                if match:
                    invalid_kwarg = match.group(1)
                info = f"Parameter '{invalid_kwarg}' was unexpected"

            elif "missing 1 required positional argument" in msg:
                match = re.search(r"missing 1 required positional argument: '(\w+)'", msg)
                if match:
                    invalid_kwarg = match.group(1)
                info = f"Parameter '{invalid_kwarg}' is missing"

            elif isinstance(e, KeyError):
                match = re.search(r"'(\w+)'", msg)
                if match:
                    invalid_kwarg = match.group(1)
                info = f"Parameter '{invalid_kwarg}' is missing"

            else:
                raise e

            raise SyntaxError(info)

        for behaviour in data["behaviour"]:
            try:
                method_name, args = list(behaviour.items())[0]
                method = getattr(obj, method_name, None)
                if method is None or not callable(method):
                    raise ValueError(f"'{method_name}' is not a valid behaviour for a {type(obj).__name__}")
                if not isinstance(args, dict):
                    raise ValueError(f"Parameters for '{method_name}' have to be in a key-value format")
                method(**args)

            except Exception as e:
                msg = str(e)
                
                if "got an unexpected keyword argument" in msg:
                    match = re.search(r"(\w+)\(\) got an unexpected keyword argument '(\w+)'", msg)
                    if match:
                        method = match.group(1)
                        invalid_kwarg = match.group(2)
                    info = f"Parameter '{invalid_kwarg}' for '{method}' was unexpected"

                elif "missing 1 required positional argument" in msg:
                    match = re.search(r"(\w+)\(\) missing 1 required positional argument: '(\w+)'", msg)
                    if match:
                        method = match.group(1)
                        invalid_kwarg = match.group(2)
                    info = f"'{method}' is missing '{invalid_kwarg}' parameter"

                else:
                    raise e

                raise SyntaxError(info)

        return obj

def bulk_implement(directory: str | pathlib.Path, datapack: beet.DataPack) -> None:
    """
    Looks for yaml files in a directory and implements all of them into a datapack

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
