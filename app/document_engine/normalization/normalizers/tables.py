from typing import cast

from app.document_engine.normalization.models.blocks import (
    NormalizedTable,
    NormalizedTableStyle,
    NormalizedRow,
    NormalizedRowStyle,
    NormalizedCell,
    NormalizedCellStyle,
    NormalizedTableWidth,
    NormalizedTableBorder,
)
from app.document_engine.normalization.normalizers.paragraphs import normalize_paragraph
from app.document_engine.normalization.errors import NormalizationFormatError
from app.document_engine.normalization.normalizers.shared import normalize_margins
from app.document_engine.normalization.style_defaults import (
    DEFAULT_TABLE_WIDTH,
    DEFAULT_TABLE_BORDER,
    DEFAULT_TABLE_STYLE,
    DEFAULT_ROW_STYLE,
    DEFAULT_CELL_STYLE,
)

from app.document_engine.parser.models.blocks import TableNode, TableRowStyle, TableCellStyle
from app.document_engine.parser.models.styles import TableBorderStyle

from app.document_engine.enums.enums import TableWidthType, TableBorderStyleEnum, TableCellShading, VerticalAlignment
from app.document_engine.utils.overlay_dataclass import overlay_dataclass_strict

def normalize_table_width(value: int | None, type: str | None) -> NormalizedTableWidth:
    if type is None:
        return DEFAULT_TABLE_WIDTH
    
    try:
        return NormalizedTableWidth(
            value=value,
            type=TableWidthType(type),
        )
    except ValueError as e:
        raise NormalizationFormatError(
            f"Invalid table width attribute: type '{type}', value '{value}'."
        ) from e


def normalize_table_border(border: TableBorderStyle | None) -> NormalizedTableBorder:
    if border is None:
        return DEFAULT_TABLE_BORDER
    
    try:
        parsed_style = NormalizedTableBorder(
            # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
            style=cast(TableBorderStyleEnum, TableBorderStyleEnum(border.style) \
                if border.style is not None \
                else None),
            size=cast(int, border.size),
            color=cast(str, border.color),
        )
    except ValueError as e:
        raise NormalizationFormatError(
            f"Invalid border style: '{border.style}'."
        ) from e

    return overlay_dataclass_strict(
        DEFAULT_TABLE_BORDER,
        parsed_style,
    )
    

def normalize_row_style(row_style: TableRowStyle | None) -> NormalizedRowStyle:
    if row_style is None:
        return DEFAULT_ROW_STYLE
    
    parsed_style = NormalizedRowStyle(
        # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
        height=cast(int, row_style.height),
        header=cast(bool, row_style.header),
    )

    return overlay_dataclass_strict(
        DEFAULT_ROW_STYLE,
        parsed_style,
    )


def normalize_cell_style(cell_style: TableCellStyle | None) -> NormalizedCellStyle:
    if cell_style is None:
        return DEFAULT_CELL_STYLE
    
    try:
        parsed_style = NormalizedCellStyle(
            # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
            shading=cast(TableCellShading, TableCellShading(cell_style.shading) \
                if cell_style.shading is not None \
                else None),
                shading_fill=cast(str, cell_style.shading_fill),
                margins=normalize_margins(cell_style.margins),
                grid_span=cast(int, cell_style.grid_span),
                v_alignment=cast(VerticalAlignment, VerticalAlignment(cell_style.v_alignment) \
                    if cell_style.v_alignment is not None \
                    else None),
        )
    except ValueError as e:
        raise NormalizationFormatError(
            f"Invalid cell shading type: {cell_style.shading}."
        ) from e
    
    return overlay_dataclass_strict(
        DEFAULT_CELL_STYLE,
        parsed_style,
    )

def normalize_table(table: TableNode) -> NormalizedTable:

    parsed_style = NormalizedTableStyle(
        # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
        width=normalize_table_width(
            table.style.width,
            table.style.width_type,
        ),
        autofit=cast(bool, table.style.autofit),
        border_top=normalize_table_border(table.style.border_top),
        border_bottom=normalize_table_border(table.style.border_bottom),
        border_left=normalize_table_border(table.style.border_left),
        border_right=normalize_table_border(table.style.border_right),
        border_inside_v=normalize_table_border(table.style.border_inside_v),
        border_inside_h=normalize_table_border(table.style.border_inside_h),
        margins=normalize_margins(table.style.margins),
    )

    normalized_style = overlay_dataclass_strict(
        DEFAULT_TABLE_STYLE,
        parsed_style,
    )

    normalized_rows = []
    for row in table.rows:

        normalized_cells = []

        for cell in row.cells:
            normalized_blocks = []
            for block in cell.blocks:
                normalized_blocks.append(
                    normalize_paragraph(block)
                )

            normalized_cells.append(
                NormalizedCell(
                    blocks=tuple(normalized_blocks),
                    style=normalize_cell_style(cell.style),
                )
            )

        normalized_rows.append(
            NormalizedRow(
                cells=tuple(normalized_cells),
                style=normalize_row_style(row.style)
            )
        )

    return NormalizedTable(
        rows=tuple(normalized_rows),
        style=normalized_style,
    )