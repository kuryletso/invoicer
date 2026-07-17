from app.core.errors import AppError, Layer, ErrorCategory


class ServiceError(AppError):
    layer = Layer.PERSISTENCE


class MissingRequiredPlaceholderValue(ServiceError):
    category = ErrorCategory.VALIDATION
    recoverable = True