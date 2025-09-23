import re

regex = r"^[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?)*$"

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

    # Currently missing:
    #  - correctly adding 'minecraft:' when there is a ! or #
    #  - checking for multiple ! or # when splitting

    def __init__(self, *, allow_tag, allow_negation):
        self.allow_tag = allow_tag
        self.allow_negation = allow_negation

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

        if re.match(regex, teststring) is None:
            raise ValueError(f"'{string}' does not match the pattern of a resource loactions")
        
        return builtstring

    def __call__(self, string: str) -> str:
        self.validate(string)

    def id(self, string: str) -> str:
        return string.split(":")[-1]