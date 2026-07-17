from __future__ import annotations

from decimal import Decimal

from num2words import num2words

from app.services.money import MoneyFormat


def spell_total(
        amount: Decimal,
        fmt: MoneyFormat,
        alpha_2: str,
) -> str:
    
    try:
        text = num2words(
            Decimal(amount),
            to="currency",
            lang=alpha_2,
            currency=fmt.code,
            cents=False,
            separator="",
        )
    except NotImplementedError:
        return ""
    
    return text[:1].upper() + text[1:]