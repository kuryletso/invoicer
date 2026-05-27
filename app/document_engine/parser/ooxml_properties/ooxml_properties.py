from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OOXMLRunAttributeNames:
    properties: str = "w:rPr"
    bold: str = "w:b"
    italic: str = "w:i"
    underline: str = "w:u"
    fonts: str = "w:rFonts"
    font_size: str = "w:sz"
    color: str = "w:color"


@dataclass(slots=True, frozen=True)
class OOXMLParagraphAttributeNames:
    properties: str = "w:pPr"
    alignment: str = "w:jc"
    spacing: str = "w:spacing"
    indent: str = "w:ind"
    keep_next: str = "w:keepNext"


@dataclass(slots=True, frozen=True)
class OOXMLTableCellAttributeNames:
    shading: str = "w:shd"
    margins: str = "w:tcMar"
    grid_span: str = "w:gridSpan"
    v_alignment: str = "w:vAlign"


@dataclass(slots=True, frozen=True)
class OOXMLTableRowAttributeNames:
    height: str = "w:trHeight"
    header: str = "w:tblHeader"


@dataclass(slots=True, frozen=True)
class OOXMLTableAttributeNames:
    properties: str = "w:tblPr"
    width: str = "w:tblW"
    layout: str = "w:tblLayout"
    borders: str = "w:tblBorders"
    margins: str = "w:tblCellMar"


@dataclass(slots=True, frozen=True)
class OOXMLStyleAttributeNames:
    style: str = "w:style"
    name: str = "w:name"
    based_on: str = "w:basedOn"