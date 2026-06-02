class NormalizationError(Exception):
    """Base normalization exception."""


class NormalizationFormatError(NormalizationError):
    """Malformed parsed object."""


class NormalizationUsageError(NormalizationError):
    """Incorrect usage of normalization assets."""