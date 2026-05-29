from enum import StrEnum
from dataclasses import dataclass

from app.document_engine.parser.models.blocks import BlockNode


class HeaderFooterType(StrEnum):
    DEFAULT = "default"
    FIRST = "first"
    EVEN = "even"


@dataclass(slots=True, frozen=True)
class HeaderFooterNode:
    type: HeaderFooterType
    blocks: list[BlockNode]