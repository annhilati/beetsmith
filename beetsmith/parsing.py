import re
import yaml
import beet
import pathlib
import inspect
import warnings
from pydantic import BaseModel, model_validator
from typing import Optional, List, Dict
from .core import CustomItem, ArmorSet
from .models import ItemComponents

# Developer Note:
#   create_from_yaml shall be raising exceptions on problems,
#   but load_dir_and_implement shall only warn the user.

def create_from_yaml(file: str | pathlib.Path) -> CustomItem | ArmorSet:
    available_types = [CustomItem, ArmorSet]

    with open(file, 'r') as f:
        data: dict = yaml.safe_load(f)

    obj_type: type        = [type for type in available_types if type.__name__ == data["type"]][0]
    obj_params: list[str] = [name for name, param in inspect.signature(obj_type.__init__).parameters.items()]

    instance_params = {param: value for param, value in data.items() if param in obj_params}
    try:
        instance: CustomItem | ArmorSet = obj_type(**instance_params)
    except Exception as e:
        msg = str(e)
        if match := re.search(r"got an unexpected keyword argument '(\w+)'", msg):
            error_info = f"Parameter '{match.group(1)}' was unexpected"
        elif match := re.search(r"missing 1 required positional argument: '(\w+)'", msg):
            error_info = f"Parameter '{match.group(1)}' is missing"
        else:
            raise e
        
    for behaviour in data["behaviour"]:
        try:
            method_name, args = list(behaviour.items())[0]
            method = getattr(instance, method_name, None)
            if method is None or not callable(method):
                raise ValueError(f"'{method_name}' is not a valid behaviour for a {obj_type.__name__}")
            if not isinstance(args, dict):
                raise ValueError(f"Parameters for '{method_name}' have to be in a key-value format")
            method(**args)
        
        except Exception as e:
            msg = str(e)
            if match := re.search(r"(\w+)\(\) got an unexpected keyword argument '(\w+)'", msg):
                error_info = f"Parameter '{match.group(2)}' for '{match.group(1)}' was unexpected"
            elif match := re.search(r"(\w+)\(\) missing 1 required positional argument: '(\w+)'", msg):
                error_info = f"'{match.group(1)}' is missing '{match.group(2)}' parameter"
            elif match := re.search(r"(\w+)\(\) missing 1 required keyword-only argument: '(\w+)'", msg):
                error_info = f"'{match.group(1)}' is missing '{match.group(2)}' parameter"
            elif "'str' object has no attribute 'items'" in msg:
                error_info = "'behaviour' parameter has to be a list"
            else:
                raise e
            raise SyntaxError(error_info)

    return instance

def bulk_implement(directory: str | pathlib.Path, datapack: beet.DataPack, allow_raises: bool = False) -> None:
    """
    Looks for yaml files in a directory and implements all of them into a datapack

    #### Parameters:
        - datapack (DataPack): A beet datapack object
        - directory (str): Directory path with desired files
    """
    directory = pathlib.Path(directory) if not isinstance(directory, pathlib.Path) else directory
    files = [filepath for filepath in directory.glob("*.yml")] + [filepath for filepath in directory.glob("*.yaml")]

    if allow_raises:
        for file in files:
            obj = create_from_yaml(file)
            obj.implement(datapack)

    else:
        for file in files:
            try: 
                obj = create_from_yaml(file)
                obj.implement(datapack)

            except Exception as e:
                warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)
