class BlueprintError(Exception):
    """Base blueprint exception."""


class PlaceholderSyntaxError(BlueprintError):
    """Invalid placeholder syntax."""


class BlueprintBuilderError(BlueprintError):
    """Internal error during blueprint building."""