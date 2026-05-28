from dataclasses import dataclass
from zipfile import ZipFile
from pathlib import Path
from os import PathLike

from lxml import etree # type: ignore

from app.document_engine.parser.errors import ParserFormatError


@dataclass(slots=True, frozen=True)
class DocxPaths:
    document: str = "word/document.xml"
    styles: str = "word/styles.xml"
    numbering: str = "word/numbering.xml"
    relationships: str = "word/_rels/document.xml.rels"


class DocxArchive:
    def __init__(self, path: str | PathLike[str]) -> None:
        self.path = Path(path)
        self.zip = ZipFile(path)

    _SAFE_PARSER = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        huge_tree=False,
    )

    def read_xml(self, archive_path: str) -> etree._Element:
        try:
            data = self.zip.read(archive_path)
        except KeyError as e:
            raise ParserFormatError(
                f"Missing XML part: {archive_path}."
            ) from e
        
        try:
            return etree.fromstring(data, parser=self._SAFE_PARSER)
        except etree.XMLSyntaxError as e:
            raise ParserFormatError(
                f"Invalid XML in part: {archive_path}."
            ) from e
    
    def read_bytes(self, archive_path: str) -> bytes:
        return self.zip.read(archive_path)
    
    def exists(self, archive_path: str) -> bool:
        return archive_path in self.zip.namelist()
    
    def close(self) -> None:
        self.zip.close()