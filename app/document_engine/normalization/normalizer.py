from app.document_engine.parser.models.inlines import RunNode
from app.document_engine.parser.models.blocks import ParagraphNode, TableNode, TableRowNode, TableCellNode, SectionBreakNode

def normalize_blocks(blocks: list[ParagraphNode | TableNode | SectionBreakNode]) -> list[]