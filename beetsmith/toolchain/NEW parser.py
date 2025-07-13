from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any, Dict, List, Optional
from beetsmith.core.classes import *

available_types = [CustomItem, ArmorSet]

# Helfermodel für einzelne Behaviour-Einträge
def available_types_names():
    return [t.__name__ for t in available_types]

class Behaviour(BaseModel):
    __root__: Dict[str, Dict[str, Any]]

    @field_validator("__root__")
    def single_entry(cls, v):
        if len(v) != 1:
            raise ValueError("Jedes Behaviour muss genau einen Methodennamen als Key enthalten")
        name, args = next(iter(v.items()))
        if not isinstance(args, dict):
            raise ValueError(f"Parameter für '{name}' müssen als Key-Value-Dict angegeben werden")
        return v

class DefinitionModel(BaseModel):
    type:       str
    name:       str
    params:     Dict[str, Any]              = Field(default_factory=dict)
    behaviour:  Optional[List[Behaviour]]   = Field(default_factory=list)
    components: Optional[Dict[str, Any]]    = Field(default_factory=dict)

    @field_validator("type")
    def valid_type(cls, v):
        if v not in available_types_names():
            raise ValueError(f"Unbekannter Typ '{v}'")
        return v

    @model_validator(mode="before")
    def split_params(cls, values):
        # Extrahiere alle Felder außer type, name, behaviour, components
        reserved = {"type", "name", "behaviour", "components"}
        values['params'] = {k: values[k] for k in list(values) if k not in reserved}
        return values
