from pathlib import Path

from app.document_engine.parser.archive import DocxArchive, DocxPaths
from app.document_engine.parser.extractors.blocks import iter_blocks
from app.document_engine.parser.extractors.paragraphs import parse_paragraph
from app.document_engine.parser.extractors.sections import parse_section
from app.document_engine.parser.extractors.tables import parse_table
from app.document_engine.parser.extractors.styles import parse_styles
from app.document_engine.parser.namespaces import NS

class DocxParser:
    def __init__(self, path: Path) -> None:
        self.archive = DocxArchive(path)
        self.document_root = self.archive.read_xml(DocxPaths.document)
        self.styles_root = self.archive.read_xml(DocxPaths.styles)
        self.styles = parse_styles(self.styles_root)

    def parse(self):
        body = self.document_root.find("w:body", NS)

        if body is None:
            raise ValueError("Document body not found")
        
        result = []

        for block_type, node in iter_blocks(body):
            match block_type:
                case "paragraph":
                    result.append(parse_paragraph(node))
                case "table":
                    result.append(parse_table(node))
                case "section":
                    result.append(parse_section(node))

        return result