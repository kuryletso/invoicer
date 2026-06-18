from pathlib import Path

from app.core.diagnostics import DiagnosticCollector
from app.core.errors import AppError, Severity

from app.document_engine.parser.parser import DocxParser
from app.document_engine.normalization.structural_normalizer import StructuralNormalizer
from app.document_engine.blueprint.template_builder import TemplateBuilder, TemplateDraft
from app.document_engine.blueprint.models.template import TemplateBlueprint

from .ports import TemplateInputProvider
from .results import IngestionResult
from .errors import IngestionError


class TemplateIngestionPipeline:
    def __init__(
        self,
        inputs: TemplateInputProvider,
    ) -> None:
        self._inputs = inputs


    def ingest(
        self,
        path: Path,
    ) -> IngestionResult:
        
        diagnostics = DiagnosticCollector()

        try:
            with DocxParser(path, diagnostics=diagnostics) as parser:
                parsed = parser.parse()

            normalized = StructuralNormalizer.normalize(parsed, diagnostics)

            draft = TemplateBuilder().build_draft(
                tuple(normalized),
                default_config=self._inputs.default_template_config(),
                placeholder_defaults=self._inputs.placeholder_defaults(),
                languages=self._inputs.languages(),
                diagnostics=diagnostics,
            )

        except AppError as e:
            diagnostics.record(e.as_diagnostic(Severity.ERROR))
            raise IngestionError(
                f"Template ingestion failed in {e.layer}: {e}.",
                user_message="The template could not be processed.",
                context={"path": str(path), "cause": e.code},
            ) from e
        
        return IngestionResult(draft=draft, diagnostics=diagnostics)
    
    def finalize(
        self,
        draft: TemplateDraft,
    ) -> TemplateBlueprint:
        
        return TemplateBuilder().save_draft(draft)