from app.core.errors import AppError, Layer, ErrorCategory

class NormalizationError(AppError):
    """Base normalization exception."""
    layer = Layer.NORMALIZATION


class NormalizationFormatError(NormalizationError):
    """Malformed parsed object."""
    category = ErrorCategory.FORMAT


class NormalizationUsageError(NormalizationError):
    """Incorrect usage of normalization assets."""
    category = ErrorCategory.USAGE