import beet
import pathlib
from typing import ClassVar
from beetsmith.core.classes import *
from beetsmith.toolchain.parser import *

class YAMLDefinition(beet.YamlFile):
    "Class representing a BeetSmith YAML definition file inside a datapack"
    scope: ClassVar[beet.NamespaceFileScope] = ("beetsmith",)
    extension: ClassVar[str] = ".yaml"

def beetsmither() -> beet.Plugin:
    """Beet Plugin configurator for BeetSmith
    
    ---
    #### Usage
    ```
    from beetsmith import beet, beetsmith

    def main(ctx: beet.Context):
        ctx.require(
            beetsmither
        )
    ```
    """

    def plugin(ctx: beet.Context):
        #ctx.data.extend_namespace.append(YAMLDefinition)

        for resource_location, file in ctx.data[YAMLDefinition].items():
            load_from_yaml(file.data).implement(ctx.data)

    return plugin

def test(ctx: beet.Context):
    print(ctx.data.extend_namespace)
    ctx.data.extend_namespace.append(YAMLDefinition)