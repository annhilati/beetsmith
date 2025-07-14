import re
import yaml
import json
import pathlib
import inspect
from pydantic import BaseModel, RootModel, Field, field_validator, model_validator, ConfigDict
from typing import Any, Dict, List, Optional, ClassVar
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

    return BeetSmithDefinition(**data).object

class BeetSmithBehavior(RootModel[Dict[str, Dict[str, Any]]]):

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
    params:     Optional[Dict[str, Any]]            = Field(default_factory=dict)
    behavior:   Optional[List[BeetSmithBehavior]]   = Field(default_factory=list)
    components: Optional[Dict[str, Any]]            = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @field_validator("type")
    def valid_type(cls, v):
        if v not in [t.__name__ for t in available_types]:
            raise ValueError(f"Unknown type '{v}'")
        return v

    @model_validator(mode="before")
    def split_params(cls, values: dict):
        
        obj_cls: type = next(t for t in available_types if t.__name__ == values["type"])

        p = [name for name, param in inspect.signature(obj_cls.__init__).parameters.items()]

        values["params"] = params = {key: value for key, value in values.items() if key in p}

        for k in params:
            values.pop(k)

        return values

    @property
    def object(self) -> CustomItem | ArmorSet:
        "Returns an Instance of the object described in the definition."

        obj_cls: type = next(t for t in available_types if t.__name__ == self.type)
        try:
            instance: CustomItem | ArmorSet = obj_cls(**self.params)
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

class BeetSmithDefinitionFile(beet.YamlFile):
    "Class representing a BeetSmith YAML definition file inside a datapack."
    
    scope: ClassVar[beet.NamespaceFileScope] = ("beetsmith",)
    extension: ClassVar[str] = ".yaml"
    data: ClassVar[beet.FileDeserialize[BeetSmithDefinition]] = beet.FileDeserialize()

    def __post_init__(self):
        super().__post_init__()
        self.decoder = BeetSmithDefinitionFile.decoder
        self.encoder = BeetSmithDefinitionFile.encoder

    @staticmethod
    def decoder(str: str) -> BeetSmithDefinition:
        try:
            data: dict = yaml.safe_load(str)
        except:
            data: dict = json.loads(str)

        return BeetSmithDefinition(**data)

    @staticmethod
    def encoder(data: BeetSmithDefinition) -> str:
        return yaml.dump(data.model_dump())
    
    @property
    def instance(self) -> CustomItem | ArmorSet:
        return self.data.object
