import re

regex = r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?:[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?(?:\/[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)*$"

class ResourceLocationChecker:
    def __init__(self, *, allow_tag, allow_negation):
        self.allow_tag = allow_tag
        self.allow_negation = allow_negation
        self.require_namespace = True

    def validate(self, string: str) -> str:
        
        build = string
        if self.require_namespace and not ":" in build:
            build = "minecraft:" + build

        # Testing
        test = build
        if self.allow_negation:
            test = test.split("!")[-1]

        if self.allow_tag:
            test = test.split("#")[-1]

        if re.match(regex, test) is None:
            raise ValueError(f"'{string}' does not match the pattern of a resource loactions")
        
        return build

    def __call__(self, string: str) -> str:
        self.validate(string)

    def id(self, string: str) -> str:
        return string.split(":")[-1]