import beet
import pathlib
from .core import *
from .parsing import *

def beetsmither(definitions_dir: str | pathlib.Path = "src/beetsmith") -> beet.Plugin:
    """Beet Plugin configurator for BeetSmith
    
    #### Usage
    ```
    from beetsmith import beet, beetsmith

    def main(ctx: beet.Context):
        ctx.require(
            beetsmith(definitions_dir="beetsmith")
        )
    ```
    """

    def plugin(ctx: beet.Context):
        bulk_implement(directory=definitions_dir, datapack=ctx.data)

    return plugin