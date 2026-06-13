from __future__ import annotations

from app.document_engine.blueprint.template_builder import TemplateBuilderContext
from app.document_engine.blueprint.builders.margins import margins_bp_from_normalized
from app.document_engine.blueprint.builders.paragraph import paragraph_bp_from_normalized
from app.document_engine.blueprint.models.table import (
    TableBlueprint,
    RowBlueprint,
    CellBlueprint,
    TableStyleBlueprint,
    RowStyleBlueprint,
    CellStyleBlueprint,
    TableWidthBlueprint,
    TableBorderBlueprint
)

from app.document_engine.normalization.models.blocks import (
    NormalizedTable,
    NormalizedRow,
    NormalizedCell,
    NormalizedTableStyle,
    NormalizedRowStyle,
    NormalizedCellStyle,
    NormalizedTableWidth,
    NormalizedTableBorder,
    NormalizedParagraph,
)


def table_border_bp_from_normalized(
    normalized: NormalizedTableBorder,
) -> TableBorderBlueprint:
    
    return TableBorderBlueprint(
        style=normalized.style,
        size=normalized.size,
        color=normalized.color,
    )


def table_width_bp_from_normalized(
    normalized: NormalizedTableWidth,
) -> TableWidthBlueprint:
    
    return TableWidthBlueprint(
        value=normalized.value,
        type=normalized.type,
    )


def cell_style_bp_from_normalized(
    normalized: NormalizedCellStyle,
) -> CellStyleBlueprint:
    
    return CellStyleBlueprint(
        shading=normalized.shading,
        shading_fill=normalized.shading_fill,
        margins=margins_bp_from_normalized(normalized.margins),
        grid_span=normalized.grid_span,
        v_alignment=normalized.v_alignment,
    )


def cell_bp_from_normalized(
    normalized: NormalizedCell,
    context: TemplateBuilderContext,
) -> CellBlueprint:
    
    style = cell_style_bp_from_normalized(normalized.style)

    blocks = []
    for block in normalized.blocks:
        if isinstance(block, NormalizedParagraph):
            blocks.append(
                paragraph_bp_from_normalized(
                    block,
                    context,
                )
            )

        elif isinstance(block, NormalizedTable):
            blocks.append(
                table_bp_from_normalized(
                    block,
                    context,
                )
            )

    return CellBlueprint(
        blocks=tuple(blocks),
        style=style,
    )


def row_style_from_normalized(
    normalized: NormalizedRowStyle,
) -> RowStyleBlueprint:
    
    return RowStyleBlueprint(
        height=normalized.height,
        header=normalized.header,
    )


def row_bp_from_normalized(
    normalized: NormalizedRow,
    context: TemplateBuilderContext,
) -> RowBlueprint:
    
    style = row_style_from_normalized(normalized.style)

    cells = []
    for cell in normalized.cells:
        cells.append(
            cell_bp_from_normalized(
                cell,
                context,
            )
        )

    return RowBlueprint(
        cells=tuple(cells),
        style=style,
    )


def table_style_bp_from_normalized(
    normalized: NormalizedTableStyle,
) -> TableStyleBlueprint:
    
    return TableStyleBlueprint(
        width=table_width_bp_from_normalized(normalized.width),
        autofit=normalized.autofit,
        border_top=table_border_bp_from_normalized(normalized.border_top),
        border_bottom=table_border_bp_from_normalized(normalized.border_bottom),
        border_left=table_border_bp_from_normalized(normalized.border_left),
        border_right=table_border_bp_from_normalized(normalized.border_right),
        border_inside_v=table_border_bp_from_normalized(normalized.border_inside_v),
        border_inside_h=table_border_bp_from_normalized(normalized.border_inside_h),
        margins=margins_bp_from_normalized(normalized.margins),
    )


def table_bp_from_normalized(
    normalized: NormalizedTable,
    context: TemplateBuilderContext,
) -> TableBlueprint:
    
    style = table_style_bp_from_normalized(normalized.style)

    rows = []
    for row in normalized.rows:
        rows.append(
            row_bp_from_normalized(
                row,
                context,
            )
        )

    return TableBlueprint(
        type="table",
        rows=tuple(rows),
        style=style,
    )