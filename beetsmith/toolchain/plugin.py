import beet
import warnings
from beetsmith.core.classes import *
from beetsmith.toolchain.file import *

def beet_default(ctx: beet.Context) -> None:
    ctx.require(
        anvil()
    )

def anvil() -> beet.Plugin:
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

        if BeetSmithDefinitionFile not in ctx.data.extend_namespace:
            raise beet.PluginError("BeetSmith plugin cannot be executed")

        instances: list[Implementable] = []

        for resource_location, file in ctx.data[BeetSmithDefinitionFile].items():
            try:
                instances.append(file.instance)

            except Exception as e:
                raise e # Debug
                warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)
            
        for instance in instances:
            try:
                instance.implement(ctx.data)

            except Exception as e:
                raise e # Debug
                warnings.warn(f"File '{file}' could not be implemented: {e}", category=UserWarning)

        # del ctx.data[YAMLDefinition]

    return plugin

def requirements(ctx: beet.Context):
    "Beet plugin fullfilling requirements for the BeetSmith plugin"
    ctx.data.extend_namespace.append(BeetSmithDefinitionFile)