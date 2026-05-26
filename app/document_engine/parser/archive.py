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
    relationships: str = "word/_rel/document.xml.rels"
    headers: str = "word/header1.xml"
    footers: str = "word/footer1.xml"


class DocxArchive:
    def __init__(self, path: str | PathLike[str]) -> None:
        self.path = Path(path)
        self.zip = ZipFile(path)

    def read_xml(self, archive_path: str) -> etree._Element:
        data = self.zip.read(archive_path)
        return etree.fromstring(data)
    
    def read_bytes(self, archive_path: str) -> bytes:
        return self.zip.read(archive_path)
    
    def exists(self, archive_path: str) -> bool:
        return archive_path in self.zip.namelist()
    
    def close(self) -> None:
        self.zip.close()