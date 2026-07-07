from app.core.errors import AppError, Layer, ErrorCategory


class RenderingError(AppError):
    """Base rendering exception."""
    layer = Layer.RENDER


class PackageError(RenderingError):
    category = ErrorCategory.INTERNAL


class PlaceholderError(RenderingError):
    category = ErrorCategory.VALIDATION