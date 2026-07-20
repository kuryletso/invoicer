from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from app.document_engine.enums.enums import MoneySymbolPosition


def group(
        digits: str,
        separator: str,
) -> str:
    
    if not separator or len(digits) <= 3:
        return digits
    
    head = len(digits) % 3 or 3
    parts = [digits[:head]]
    parts.extend(digits[i:i+3] for i in range(head, len(digits), 3))
    return separator.join(parts)


def format_quantity(
        value: Decimal,
        fmt: MoneyFormat,
) -> str:
    
    negative = value < 0
    text = format(abs(value).normalize(), "f")
    int_part, _, frac = text.partition(".")
    out = group(int_part, fmt.grouping_separator)
    if frac:
        out += fmt.decimal_separator + frac
    return "-" + out if negative else out


@dataclass(slots=True, frozen=True)
class MoneyFormat:
    code: str
    decimal_places: int
    decimal_separator: str
    grouping_separator: str
    symbol_position: MoneySymbolPosition
    symbol_spacing: bool
    symbols: Mapping[str, str]


    def format(
        self,
        amount: Decimal,
        language: str,
        append: bool,
    ) -> str:
        
        value = self._quantize(amount)
        sign = "-" if value < 0 else ""
        text = self._plain(abs(value))
        if append:
            text = self._attach(text, self.symbols.get(language) or self.code)
        return sign + text
    

    def format_all(
        self,
        amount: Decimal,
        languages: tuple[str, ...],
        append: bool,
    ) -> dict[str, str]:
        return {lang: self.format(amount, lang, append) for lang in languages}
    

    def _quantize(
        self,
        amount: Decimal,
    ) -> Decimal:
        
        return amount.quantize(
            Decimal(1).scaleb(-self.decimal_places),
            rounding=ROUND_HALF_UP,
        )
    
    def _plain(
            self,
            value: Decimal,
    ) -> str:
        
        int_part, _, frac = f"{value:.{self.decimal_places}f}".partition(".")
        int_part = self._group(int_part)
        return int_part + self.decimal_separator + frac if frac else int_part
    

    def _group(
            self,
            digits: str,
    ) -> str:
        
        # if not self.grouping_separator or len(digits) <= 3:
        #     return digits
        
        # head = len(digits) % 3 or 3
        # parts = [digits[:head]]
        # parts.extend(digits[i:i + 3] for i in range(head, len(digits), 3))
        # return self.grouping_separator.join(parts)

        return group(digits, self.grouping_separator)
    
    def _attach(
            self,
            text: str,
            symbol: str,
    ) -> str:
        
        gap = " " if self.symbol_spacing else ""
        if self.symbol_position is MoneySymbolPosition.PREFIX:
            return f"{symbol}{gap}{text}"
        return f"{text}{gap}{symbol}"