class BlueprintError(Exception):
    """Base blueprint exception."""


class PlaceholderSyntaxError(BlueprintError):
    """Invalid placeholder syntax."""