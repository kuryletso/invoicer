from app.core.errors import AppError, Layer, ErrorCategory


class BlueprintError(AppError):
    """Base blueprint exception."""
    layer = Layer.BLUEPRINT


class PlaceholderSyntaxError(BlueprintError):
    """Invalid placeholder syntax."""
    category = ErrorCategory.FORMAT


class BlueprintBuilderError(BlueprintError):
    """Internal error during blueprint building."""
    category = ErrorCategory.INTERNAL