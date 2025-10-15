import beet
import warnings
import pydantic
from beetsmith.library.item import Item
from beetsmith.toolchain.file import BeetSmithDefinitionFile

class BeetSmithConfig(pydantic.BaseModel):
    auto: bool = True
    debug: bool = False

@beet.configurable(validator=BeetSmithConfig)
def beet_default(ctx: beet.Context, opts: BeetSmithConfig) -> None:
    if opts.auto:
        ctx.require(
            auto_item(debug=opts.debug)
        )

def auto_item(debug: bool = False) -> beet.Plugin:

    def plugin(ctx: beet.Context):

        if BeetSmithDefinitionFile not in ctx.data.extend_namespace:
            raise beet.PluginError("BeetSmith plugin cannot be executed: The requirements are missing in require")

        instances: list[Item] = []

        for resource_location, file in ctx.data[BeetSmithDefinitionFile].items():
            try:
                instances.append(file.instance)

            except Exception as e:
                if debug:
                    raise e
                warnings.warn(f"File '{file}' could not be loaded and implemented: {e}", category=UserWarning)
            
        for instance in instances:
            try:
                instance.implement(ctx.data)

            except Exception as e:
                if debug:
                    raise e
                warnings.warn(f"File '{file}' could not be implemented: {e}", category=UserWarning)

        # del ctx.data[YAMLDefinition]

    return plugin

def requirements(ctx: beet.Context):
    "Beet plugin fullfilling requirements for the BeetSmith plugin"
    ctx.data.extend_namespace.append(BeetSmithDefinitionFile)