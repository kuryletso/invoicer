from dataclasses import dataclass

from app.core.diagnostics import DiagnosticCollector
from app.document_engine.blueprint.template_builder import TemplateDraft


@dataclass(slots=True)
class IngestionResult:
    draft: TemplateDraft
    diagnostics: DiagnosticCollector


@dataclass(slots=True)
class RenderingResult:
    docx: bytes | None
    diagnostics: DiagnosticCollector