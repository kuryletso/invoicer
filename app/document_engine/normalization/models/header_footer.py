from dataclasses import dataclass

from app.document_engine.normalization.models.blocks import NormalizedBlock
from app.document_engine.enums.enums import HeaderFooterType


@dataclass(slots=True, frozen=True)
class NormalizedHeaderFooter:
    type: HeaderFooterType
    blocks: tuple[NormalizedBlock, ...]


@dataclass(slots=True, frozen=True)
class NormalizedHeaderFooterGroup:
    default: NormalizedHeaderFooter | None
    first: NormalizedHeaderFooter | None
    even: NormalizedHeaderFooter | None