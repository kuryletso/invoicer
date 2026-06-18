from dataclasses import dataclass

from app.assets.service import AssetService
from app.core.diagnostics import DiagnosticCollector
from app.document_engine.parser.archive import DocxArchive
from app.document_engine.parser.relationships import RelationshipResolver
from app.document_engine.parser.style_resolver.style_resolver import StyleResolver


@dataclass(slots=True, frozen=True)
class ParserContext:
    archive: DocxArchive
    relationships: RelationshipResolver
    asset_service: AssetService
    style_resolver: StyleResolver
    diagnostics: DiagnosticCollector