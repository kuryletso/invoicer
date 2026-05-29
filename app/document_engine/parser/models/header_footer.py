from dataclasses import dataclass

from app.document_engine.enums.enums import HeaderFooterType
from app.document_engine.parser.models.blocks import BlockNode


@dataclass(slots=True, frozen=True)
class HeaderFooterNode:
    type: HeaderFooterType
    blocks: list[BlockNode]