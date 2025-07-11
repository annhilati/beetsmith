import beet
import warnings
from typing import ClassVar
from beetsmith.core.classes import *
from beetsmith.toolchain.parser import *

class YAMLDefinition(beet.YamlFile):
    "Class representing a BeetSmith YAML definition file inside a datapack."
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

        if YAMLDefinition not in ctx.data.extend_namespace:
            raise beet.PluginError("BeetSmith plugin cannot be executed")

        instances: list[Implementable] = []
        definition_files: list[str] = []

        try:
            for resource_location, file in ctx.data[YAMLDefinition].items():
                instances.append(load_from_yaml(file.data))
                definition_files.append(resource_location)
                
            for instance in instances:
                instance.implement(ctx.data)

        except Exception as e:
            raise e # Debug
            warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)

    return plugin

def requirements(ctx: beet.Context):
    "Beet plugin fullfilling requirements for the BeetSmith plugin"
    ctx.data.extend_namespace.append(YAMLDefinition)