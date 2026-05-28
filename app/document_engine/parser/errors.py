class ParserError(Exception):
    """Base parser exception."""


class ParserFormatError(ParserError):
    """Malformed DOCX structure."""


class ParserSecurityError(ParserError):
    """Security validation failed."""


class ParserAssetError(ParserError):
    """Asset/image/media problem."""


class StyleResolutionError(ParserError):
    """Style resolution failed."""


class UnsupportedFeatureError(ParserError):
    """Feature intentionally unsupported."""