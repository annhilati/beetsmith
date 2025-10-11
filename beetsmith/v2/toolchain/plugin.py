import beet
import warnings
from beetsmith.v2.library.item import Item
from beetsmith.v2.toolchain.file import BeetSmithDefinitionFile
from pydantic import BaseModel

class BeetSmithConfig(BaseModel):
    ...

@beet.configurable(validator=BeetSmithConfig)
def beet_default(ctx: beet.Context, opts: BeetSmithConfig) -> None:
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
            raise beet.PluginError("BeetSmith plugin cannot be executed: The requirements are missing in require")

        instances: list[Item] = []

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