from dataclasses import dataclass, field
from app.core.errors import Layer, Severity


@dataclass(slots=True, frozen=True)
class Diagnostic:
    layer: Layer
    severity: Severity
    code: str
    message: str
    context: dict | None = None


@dataclass(slots=True)
class DiagnosticCollector:
    items: list[Diagnostic] = field(default_factory=list)

    def warn(
        self,
        layer: Layer,
        code: str,
        message: str,
        **context,
    ) -> None:
        
        self.items.append(
            Diagnostic(
                layer,
                Severity.WARNING,
                code,
                message,
                context or None,
            )
        )

    def record(
        self,
        diagnostic: Diagnostic,
    ) -> None:
        
        self.items.append(diagnostic)

    @property
    def warnings(self):
        return [
            d for d in self.items
            if d.severity is Severity.WARNING
        ]
    
    @property
    def has_errors(self):
        return any(
            d.severity is Severity.ERROR
            for d in self.items
        )