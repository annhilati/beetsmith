import re
import yaml, json
import pathlib
import beet
import inspect
from pydantic import BaseModel, RootModel, Field, field_validator, model_validator, ConfigDict
from typing import Any, Dict, List, Optional, ClassVar
from beetsmith.library.item import Item

_available_types = [Item]

def parse_from_file(file: str | pathlib.Path, /) -> Item:
    """Instanciates an Item object from a file.

    Supported are YAML and JSON.
    """

    suffix = file.suffix if isinstance(file, pathlib.Path) else file.split(":")[-1]

    with open(file, 'r', encoding="utf-8") as f:
        match suffix:
            case ".yml" | "yaml":
                data: dict = yaml.safe_load(f)
            case ".json":
                data: dict = json.load(f)

    return BeetSmithDefinition(**data).instance()

class BeetSmithBehavior(RootModel[Dict[str, Dict[str, Any]]]):

    @field_validator('root')
    def single_entry(cls, pair: dict[str, dict]):
        if len(pair) != 1:
            raise ValueError("Behavior should have exactly one key")
        name, args = next(iter(pair.items()))
        if not isinstance(args, dict):
            raise ValueError(f"Parameters for '{name}' have to be in a key-value format")
        return pair

class BeetSmithDefinition(BaseModel):
    type:       str
    params:     Optional[Dict[str, Any]]            = Field(default_factory=dict)
    behavior:   Optional[List[BeetSmithBehavior]]   = Field(default_factory=list)
    components: Optional[Dict[str, Any]]            = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @field_validator("type")
    def valid_type(cls, type):
        if type not in [t.__name__ for t in _available_types]:
            raise ValueError(f"Unknown BeetSmith definition type '{type}'")
        return type

    @model_validator(mode="before")
    def split_params(cls, values: dict):
        
        obj_cls: type = next(t for t in _available_types if t.__name__ == values["type"])

        cls_params = [name for name, param in inspect.signature(obj_cls.__init__).parameters.items()]

        values["params"] = {key: value for key, value in values.items() if key in cls_params}

        return values

    def instance(self) -> Item:
        "Returns an Instance of the object described in the definition."

        obj_cls: type = next(t for t in _available_types if t.__name__ == self.type)
        try:
            instance: Item = obj_cls(**self.params)
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
        for component, override in self.components.items():
            current = getattr(instance.components, component, None)
            if isinstance(current, dict) and isinstance(override, dict):
                current.update(override)
            elif isinstance(current, str) and isinstance(override, str):
                setattr(instance.components, component, override)
            elif current is None:
                setattr(instance.components, component, override)
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
    def instance(self) -> Item:
        return self.data.instance()
