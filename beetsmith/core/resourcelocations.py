"Submodule for working with resource locations"

# DEVELOPMENT STATUS
# -----------------------
# There's already a good concept and implementation for abstracting resource location checkers.
# Although, due to the high complexity that such strings can have and the many combinations that are not allowed,
# there is still a lot of specific situations where validation falsly completes.
# Missing are:
#  - correctly adding 'minecraft:' when there are modifiers like `!` or `#`
#  - toggle dots
#  - raise on multiple consecutive dots

import re

regex = r"^[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)*$"

class ResourceLocationChecker:
    """Class for configurating a functor that can be used to check if a string is a valid resource location.

    Example
    ---------
    ```
    componentQueryValidator = ResourceLocationChecker(allow_tag=True, allow_negation=False)
    componentQueryValidator("minecraft:stone")   # -> minecraft:stone
    componentQueryValidator("stone")             # -> minecraft:stone
    componentQueryValidator("#minecraft:stones") # -> #minecraft:stones
    ```
    """

    def __init__(self, *,
                 allow_tag: bool = False,
                 allow_negation: bool = False,
                 allow_paths: bool = True
                 ):
        self.allow_tag = allow_tag
        self.allow_negation = allow_negation
        self.allow_paths = allow_paths

    def validate(self, string: str) -> str:
        
        # Building
        builtstring = string
        if not ":" in builtstring:
            builtstring = "minecraft:" + builtstring

        # Testing
        teststring = builtstring
        if self.allow_negation:
            teststring = teststring.split("!")[-1]

        if self.allow_tag:
            teststring = teststring.split("#")[-1]

        if not self.allow_paths and "/" in teststring:
            raise ValueError(f"'{string}' resource loactions cannot contain paths")

        if re.match(regex, teststring) is None:
            raise ValueError(f"'{string}' does not match the pattern of a resource loactions")
        
        return builtstring

    def __call__(self, string: str) -> str:
        return self.validate(string)
    
ensureNoSpecialRL   = ResourceLocationChecker(allow_tag=False, allow_negation=False, allow_paths=False)
ensureNoTagPathRL   = ResourceLocationChecker(allow_tag=False, allow_negation=False, allow_paths=True)
ensureTagLikeRL     = ResourceLocationChecker(allow_tag=True,  allow_negation=False, allow_paths=True)
ensureComponent     = ResourceLocationChecker(allow_tag=False, allow_negation=True,  allow_paths=True)