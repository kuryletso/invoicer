from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field


Values = Mapping[str, str]      # language_code : value


@dataclass(slots=True, frozen=True)
class InvoiceLineRow:
    values: Mapping[str, Values]        # column key (invl_*) : {lang : value}


@dataclass(slots=True, frozen=True)
class InvoiceTableData:
    rows: tuple[InvoiceLineRow, ...]
    show_tax: bool
    subtotal: Values
    total_tax: Values | None
    total: Values
    labels: Mapping[str, Values]        # localized header + summary labels


@dataclass(slots=True, frozen=True)
class RenderContext:

    scalars: Mapping[str, Values] = field(default_factory=dict)

    table: InvoiceTableData | None = None

    def override(
        self,
        *,
        scalars: Mapping[str, Values] | None = None,
        table: InvoiceTableData | None = None,
    ) -> RenderContext:
        
        return RenderContext(
            scalars={**self.scalars, **(scalars or {})},
            table=table if table is not None else self.table,
        )