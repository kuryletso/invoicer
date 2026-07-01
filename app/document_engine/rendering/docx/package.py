import io
import zipfile
from lxml import etree

from app.document_engine.rendering.docx.content_types_xml import build_content_types
from app.document_engine.rendering.docx.rels import RelationshipRegistry
from app.document_engine.rendering.docx.constants import (
    IMAGE_CONTENT_TYPES,
    ROOT_RELS,
)

from app.document_engine.rendering.errors import PackageError

class DocxPackage:
    def __init__(self) -> None:
        self._parts: dict[str, bytes] = {}
        self._overrides: dict[str, str] = {}
        self._extensions: dict[str, str] = {}
        self._doc_rels = RelationshipRegistry()

    def add_xml(
        self,
        path: str,
        element: etree._Element,
        content_type: str,
    ) -> None:
        
        self._parts[path] = etree.tostring(
            element,
            xml_declaration=True,
            encoding="UTF-8",
            standalone=True,
        )
        self._overrides["/" + path] = content_type

    def add_image(
        self,
        path: str,
        data: bytes,
    ) -> None:
        
        self._parts[path] = data
        ext = path.rsplit(".", 1)[-1].lower()
        if ext not in IMAGE_CONTENT_TYPES:
            raise PackageError(
                f"Unsupported image extension [{ext}] in file {path}."
            )
        
        self._extensions[ext] = IMAGE_CONTENT_TYPES[ext]

    def add_rels(
        self,
        path: str,
        element: etree._Element,
    ) -> None:
        
        self._parts[path] = etree.tostring(
            element,
            xml_declaration=True,
            encoding="UTF-8",
            standalone=True,
        )

    def add_document_relationship(
        self,
        rtype: str,
        target: str,
    ) -> str:
        
        return self._doc_rels.add(rtype, target)


    def to_bytes(self) -> bytes:

        content_types = build_content_types(self._overrides, self._extensions)

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(
                "[Content_Types].xml",
                etree.tostring(
                    content_types,
                    xml_declaration=True,
                    encoding="UTF-8",
                    standalone=True,
                )
            )
            zf.writestr("_rels/.rels", ROOT_RELS)

            doc_rels = self._doc_rels.build()
            if doc_rels is not None:
                zf.writestr(
                    "word/_rels/document.xml.rels",
                    etree.tostring(
                        doc_rels,
                        xml_declaration=True,
                        encoding="UTF-8",
                        standalone=True,
                    )
                )


            for path, data in self._parts.items():
                zf.writestr(path, data)

        return buf.getvalue()