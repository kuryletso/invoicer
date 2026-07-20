from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from num2words import num2words

from app.services.money import MoneyFormat


def spell_total(
        amount: Decimal,
        fmt: MoneyFormat,
        alpha_2: str,
) -> str:
    
    text = _spell_native(amount, fmt, alpha_2) or _spell_iso(amount, fmt, alpha_2)
    if not text:
        return ""
    
    return text[:1].upper() + text[1:]


def _spell_native(
        amount: Decimal,
        fmt: MoneyFormat,
        alpha_2: str,
) -> str:
    """num2words' own currency wording"""

    try:
        return num2words(
            Decimal(amount),
            to="currency",
            lang=alpha_2,
            currency=fmt.code,
            cents=False,
            separator="",
        )
    except NotImplementedError:
        return ""
    

def _spell_iso(
        amount: Decimal,
        fmt: MoneyFormat,
        alpha_2: str,
) -> str:
    """Fallback: spell the number, name the currency by its ISO code."""

    units, minor = _split(amount, fmt.decimal_places)

    try:
        words = num2words(units, lang=alpha_2)
    except NotImplementedError:
        return ""

    if fmt.decimal_places == 0:
        return f"{words} {fmt.code}"

    return f"{words} {fmt.code} {minor:0{fmt.decimal_places}d}" 


def _split(
        amount: Decimal,
        places: int,
) -> tuple[int, int]:
    
    exp = Decimal(1).scaleb(-places)
    value = amount.quantize(exp, rounding=ROUND_HALF_UP)
    units = int(value)
    minor = int((abs(value) - abs(Decimal(units))) * (10 ** places))

    return units, minor