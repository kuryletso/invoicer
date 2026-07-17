from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from app.services.invoice.data import Line


@dataclass(slots=True, frozen=True)
class LineTotals:
    net: Decimal
    tax: Decimal


@dataclass(slots=True, frozen=True)
class InvoiceTotals:
    lines: tuple[LineTotals, ...]
    subtotal: Decimal
    total_tax: Decimal
    total: Decimal
    taxed: bool


def compute_totals(
        lines: Sequence[Line],
        decimal_places: int,
) -> InvoiceTotals:
    
    exp = Decimal(1).scaleb(-decimal_places)

    per_line: list[LineTotals] = []
    for line in lines:
        net = (line.quantity * line.unit_price).quantize(exp, rounding=ROUND_HALF_UP)
        tax = (net * line.tax_rate).quantize(exp, rounding=ROUND_HALF_UP)
        per_line.append(LineTotals(net=net, tax=tax))

    subtotal = sum((t.net for t in per_line), Decimal(0))
    total_tax = sum((t.tax for t in per_line), Decimal(0))

    return InvoiceTotals(
        lines=tuple(per_line),
        subtotal=subtotal,
        total_tax=total_tax,
        total=subtotal + total_tax,
        taxed=any(line.tax_rate > 0 for line in lines),
    )