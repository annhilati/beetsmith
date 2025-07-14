import pathlib
import yaml
import json
import re
from pydantic import BaseModel, RootModel, Field, field_validator, model_validator, PrivateAttr, ConfigDict
from typing import Any, Dict, List, Optional, ClassVar, Callable
from beetsmith.core.classes import *


available_types = [CustomItem, ArmorSet]

def load_from_file(file: str | pathlib.Path, /) -> CustomItem | ArmorSet:
    """Instanciates a CustomItem or ArmorSet object from a file.

    Supported are YAML and JSON.
    """

    with open(file, 'r', encoding="utf-8") as f:
        match file.suffix:
            case ".yml" | "yaml":
                data: dict = yaml.safe_load(f)
            case ".json":
                data: dict = json.load(f)

    return BeetSmithDefinition(**data).to_object()

class BeetSmithBehaviour(RootModel[Dict[str, Dict[str, Any]]]):

    @field_validator('root')
    def single_entry(cls, v):
        if len(v) != 1:
            raise ValueError("Jedes Behaviour muss genau einen Methodennamen als Key enthalten")
        name, args = next(iter(v.items()))
        if not isinstance(args, dict):
            raise ValueError(f"Parameter für '{name}' müssen als Key-Value-Dict angegeben werden")
        return v

class BeetSmithDefinition(BaseModel):
    type:       str
    behavior:   Optional[List[BeetSmithBehaviour]]  = Field(default_factory=list)
    components: Optional[Dict[str, Any]]            = Field(default_factory=dict)
    params:    Optional[Dict[str, Any]]                      = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @field_validator("type")
    def valid_type(cls, v):
        if v not in [t.__name__ for t in available_types]:
            raise ValueError(f"Unbekannter Typ '{v}'")
        return v

    @model_validator(mode="before")
    def split_params(cls, values: dict):
        print(f"model validator", values) # Debug

        reserved = {"type", "behavior", "components"}
        params = {k: v for k, v in values.items() if k not in reserved}
        values["_params"] = params
        for k in params:
            values.pop(k)
        
        print(f"model validator", values) # Debug
        return values

    def to_object(self) -> CustomItem | ArmorSet:
        # Instanziiere das Objekt
        obj_cls: type = next(t for t in available_types if t.__name__ == self.type)
        try:
            print(self._params) # Debug
            instance: CustomItem | ArmorSet = obj_cls(**self._params)
        except TypeError as e:
            msg = str(e)
            if match := re.search(r"missing (\d+) required positional argument: '([^']+)'", msg):
                raise SyntaxError(f"Missing parameter '{match.group(2)}'")
            raise e

        # Verarbeite Behaviour
        for behavior in self.behavior:
            name, args = next(iter(behavior.root.items()))
            method = getattr(instance, name, None)
            if method is None or not callable(method):
                raise SyntaxError(f"Unknown behavior '{name}' for {self.type}")
            try:
                method(**args)
            except TypeError as e:
                msg = str(e)
                if match := re.search(r"(\w+)\(\) got an unexpected keyword argument '([^']+)'", msg):
                    raise SyntaxError(f"Parameter '{match.group(2)}' for '{match.group(1)}' was unexpected")
                if match := re.search(r"(\w+)\(\) missing .* argument: '([^']+)'", msg):
                    raise SyntaxError(f"Behaviour '{match.group(1)}' is missing parameter '{match.group(2)}'")
                raise

        # Verarbeite Components
        for comp, override in self.components.items():
            current = getattr(instance.components, comp, None)
            if isinstance(current, dict) and isinstance(override, dict):
                current.update(override)
            elif isinstance(current, str) and isinstance(override, str):
                setattr(instance.components, comp, override)
            elif current is None:
                setattr(instance.components, comp, override)
            else:
                raise NotImplementedError(f"Can't override component of type '{type(current).__name__}' with '{type(override).__name__}'")

        return instance
    
def file_decoder(str: str) -> BeetSmithDefinition:
    try:
        data: dict = yaml.safe_load(str)
    except:
        data: dict = json.load(str)

    return BeetSmithDefinition(**data)

def file_encoder(obj: BeetSmithDefinition) -> str:
    return yaml.dump(obj.model_dump())

class YAMLDefinition(beet.YamlFile):
    "Class representing a BeetSmith YAML definition file inside a datapack."
    
    scope: ClassVar[beet.NamespaceFileScope] = ("beetsmith",)
    extension: ClassVar[str] = ".yaml"
    data: ClassVar[beet.FileDeserialize[BeetSmithDefinition]] = beet.FileDeserialize()
    decoder: Callable[[str], Any] = file_decoder
    encoder: Callable[[Any], str] = file_encoder

    def __post_init__(self):
        super().__post_init__()
        self.decoder = file_decoder
        self.encoder = file_encoder
