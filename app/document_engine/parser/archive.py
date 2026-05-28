from dataclasses import dataclass
from zipfile import ZipFile
from pathlib import Path
from os import PathLike

from lxml import etree # type: ignore


@dataclass(slots=True, frozen=True)
class DocxPaths:
    document: str = "word/document.xml"
    styles: str = "word/styles.xml"
    numbering: str = "word/numbering.xml"
    relationships: str = "word/_rels/document.xml.rels"
    headers: str = "word/header1.xml"
    footers: str = "word/footer1.xml"


class DocxArchive:
    def __init__(self, path: str | PathLike[str]) -> None:
        self.path = Path(path)
        self.zip = ZipFile(path)

    _SAFE_PARSER = etree.XMLParser(resolve_entities=False, no_network=True)

    def read_xml(self, archive_path: str) -> etree._Element:
        data = self.zip.read(archive_path)
        return etree.fromstring(data, parser=self._SAFE_PARSER)
    
    def read_bytes(self, archive_path: str) -> bytes:
        return self.zip.read(archive_path)
    
    def exists(self, archive_path: str) -> bool:
        return archive_path in self.zip.namelist()
    
    def close(self) -> None:
        self.zip.close()