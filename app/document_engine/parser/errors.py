from app.core.errors import AppError, Layer, ErrorCategory


class ParserError(AppError):
    """Base parser exception."""
    layer = Layer.PARSER


class ParserFormatError(ParserError):
    """Malformed DOCX structure."""
    category = ErrorCategory.FORMAT


class ParserSecurityError(ParserError):
    """Security validation failed."""
    category = ErrorCategory.SECURITY


class ParserAssetError(ParserError):
    """Asset/image/media problem."""
    category = ErrorCategory.FORMAT


class StyleResolutionError(ParserError):
    """Style resolution failed."""
    category = ErrorCategory.INTERNAL


class UnsupportedFeatureError(ParserError):
    """Feature intentionally unsupported."""
    category = ErrorCategory.UNSUPPORTED
    recoverable = True