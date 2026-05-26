from dataclasses import dataclass

from app.assets.service import AssetService
from app.document_engine.parser.archive import DocxArchive
from app.document_engine.parser.relationships import RelationshipResolver

@dataclass(slots=True, frozen=True)
class ParserContext:
    archive: DocxArchive
    relationships: RelationshipResolver
    asset_service: AssetService