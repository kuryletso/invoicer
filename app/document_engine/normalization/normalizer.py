from app.document_engine.parser.models.blocks import ParagraphNode, TableNode, SectionBreakNode
from app.document_engine.normalization.models.sections import NormalizedSection, NormalizedSectionBuilder

type ParsedBlock = ParagraphNode | TableNode | SectionBreakNode
  

class StructuralNormalizer:
    def __init__(self, blocks: list[ParsedBlock]) -> None:
        self.parsed_blocks = blocks

    def normalize(self) -> list[NormalizedSection]:
        
        sections = []
        
        current_section = NormalizedSectionBuilder()

        for block in self.parsed_blocks:
            match block:
                case ParagraphNode:
                    current_section.blocks.append(normalize_paragraph(block))