from app.core.errors import AppError, Layer, ErrorCategory


class OrchestrationError(AppError):
    """Document engine orchestration error."""
    layer = Layer.ORCHESTRATION


class IngestionError(OrchestrationError):
    """A stage failed and ingestion could not complete."""
    category = ErrorCategory.INTERNAL


class RenderingFailedError(OrchestrationError):
    """A stage failed and rendering could not complete."""
    category = ErrorCategory.INTERNAL