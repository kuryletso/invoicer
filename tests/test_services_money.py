"""Money formatting, quantity formatting, totals arithmetic and amount-in-words."""

from decimal import Decimal

import pytest

from app.document_engine.enums.enums import MoneySymbolPosition
from app.services.invoice.data import Line
from app.services.invoice.totals import compute_totals
from app.services.money import MoneyFormat, format_quantity, group
from app.services.spell_total import spell_total


def money(
    *,
    decimal_places: int = 2,
    decimal_separator: str = ",",
    grouping_separator: str = " ",
    symbol_position: MoneySymbolPosition = MoneySymbolPosition.SUFFIX,
    symbol_spacing: bool = True,
    symbols: dict[str, str] | None = None,
    code: str = "UAH",
) -> MoneyFormat:
    return MoneyFormat(
        code=code,
        decimal_places=decimal_places,
        decimal_separator=decimal_separator,
        grouping_separator=grouping_separator,
        symbol_position=symbol_position,
        symbol_spacing=symbol_spacing,
        symbols=symbols if symbols is not None else {"UKR": "₴", "ENG": "UAH"},
    )


def line(quantity: str, unit_price: str, tax_rate: str = "0") -> Line:
    return Line(
        description={"ENG": "x"},
        unit={"ENG": "u"},
        quantity=Decimal(quantity),
        unit_price=Decimal(unit_price),
        tax_rate=Decimal(tax_rate),
    )


# --- grouping ----------------------------------------------------------------

@pytest.mark.parametrize(
    "digits, expected",
    [
        ("1", "1"),
        ("123", "123"),
        ("1234", "1 234"),
        ("12345", "12 345"),
        ("123456", "123 456"),
        ("1234567", "1 234 567"),
    ],
)
def test_group_inserts_separator_every_three_digits(digits, expected):
    assert group(digits, " ") == expected


def test_group_without_separator_is_identity():
    assert group("1234567", "") == "1234567"


# --- money -------------------------------------------------------------------

def test_format_applies_separators_and_decimals():
    assert money().format(Decimal("1234.5"), "UKR", append=False) == "1 234,50"


def test_format_appends_localized_symbol_as_suffix_with_spacing():
    assert money().format(Decimal("1234.5"), "UKR", append=True) == "1 234,50 ₴"


def test_format_prefix_without_spacing():
    fmt = money(
        decimal_separator=".",
        grouping_separator=",",
        symbol_position=MoneySymbolPosition.PREFIX,
        symbol_spacing=False,
        symbols={"ENG": "$"},
        code="USD",
    )
    assert fmt.format(Decimal("1234.5"), "ENG", append=True) == "$1,234.50"


def test_format_falls_back_to_iso_code_when_symbol_missing():
    fmt = money(symbols={})
    assert fmt.format(Decimal("5"), "UKR", append=True) == "5,00 UAH"


def test_negative_sign_precedes_the_symbol():
    """`-5,00 ₴`, never `5,00 -₴` or `₴-5,00`."""
    assert money().format(Decimal("-5"), "UKR", append=True) == "-5,00 ₴"


def test_format_rounds_half_up():
    assert money().format(Decimal("1.005"), "UKR", append=False) == "1,01"


def test_zero_decimal_places_omits_separator():
    fmt = money(decimal_places=0, symbols={})
    assert fmt.format(Decimal("1234"), "UKR", append=False) == "1 234"


def test_format_all_produces_a_value_per_language():
    assert money().format_all(Decimal("5"), ("UKR", "ENG"), append=True) == {
        "UKR": "5,00 ₴",
        "ENG": "5,00 UAH",
    }


# --- quantity ----------------------------------------------------------------

@pytest.mark.parametrize(
    "value, expected",
    [
        ("10.000", "10"),      # trailing zeros dropped
        ("1.500", "1,5"),
        ("0.125", "0,125"),
        ("2", "2"),
        ("-3.500", "-3,5"),
    ],
)
def test_format_quantity_normalizes_trailing_zeros(value, expected):
    assert format_quantity(Decimal(value), money()) == expected


def test_format_quantity_never_uses_scientific_notation():
    """Decimal('10000').normalize() is 1E+4 — must not leak into the document."""
    assert format_quantity(Decimal("10000"), money()) == "10 000"


# --- totals ------------------------------------------------------------------

def test_compute_totals_sums_lines():
    totals = compute_totals([line("10", "125.50"), line("2", "10")], decimal_places=2)

    assert totals.subtotal == Decimal("1275.00")
    assert totals.total_tax == Decimal("0")
    assert totals.total == Decimal("1275.00")
    assert totals.taxed is False


def test_compute_totals_applies_tax_per_line():
    totals = compute_totals([line("10", "125.50", "0.20")], decimal_places=2)

    assert totals.subtotal == Decimal("1255.00")
    assert totals.total_tax == Decimal("251.00")
    assert totals.total == Decimal("1506.00")
    assert totals.taxed is True


def test_line_amounts_are_rounded_before_summing():
    """Printed lines must reconcile with the printed total."""
    totals = compute_totals([line("1", "0.005"), line("1", "0.005")], decimal_places=2)

    assert [t.net for t in totals.lines] == [Decimal("0.01"), Decimal("0.01")]
    assert totals.subtotal == Decimal("0.02")


def test_empty_lines_produce_zero_totals():
    totals = compute_totals([], decimal_places=2)

    assert totals.subtotal == Decimal("0")
    assert totals.total == Decimal("0")
    assert totals.taxed is False


def test_taxed_is_false_when_every_rate_is_zero():
    totals = compute_totals([line("1", "10", "0")], decimal_places=2)
    assert totals.taxed is False


# --- amount in words ---------------------------------------------------------

def test_spell_total_declines_ukrainian_currency():
    assert spell_total(Decimal("1"), money(), "uk").startswith("Одна гривня")
    assert spell_total(Decimal("2"), money(), "uk").startswith("Дві гривні")
    assert spell_total(Decimal("5"), money(), "uk").startswith("П'ять гривень")


def test_spell_total_capitalizes_and_keeps_digits_for_minor_units():
    assert spell_total(Decimal("1234.56"), money(), "uk") == (
        "Одна тисяча двісті тридцять чотири гривні 56 копійок"
    )


def test_spell_total_treats_int_as_major_units():
    """num2words reads a bare int as minor units; the Decimal wrap must prevent it."""
    assert spell_total(1, money(), "uk") == spell_total(Decimal("1"), money(), "uk")


def test_spell_total_falls_back_to_iso_code_for_an_unsupported_currency():
    """en+CZK has no currency table in num2words; the ISO code names it instead."""
    assert spell_total(Decimal("2"), money(code="CZK"), "en") == "Two CZK 00"


def test_iso_fallback_spells_minor_units_as_padded_digits():
    assert spell_total(Decimal("1234.56"), money(code="UAH"), "en") == (
        "One thousand, two hundred and thirty-four UAH 56"
    )


def test_iso_fallback_rounds_before_splitting():
    assert spell_total(Decimal("1.005"), money(code="UAH"), "en") == "One UAH 01"


def test_iso_fallback_omits_minor_units_for_zero_decimal_currency():
    assert spell_total(Decimal("1506"), money(code="JPY", decimal_places=0), "en") == (
        "One thousand, five hundred and six JPY"
    )


def test_native_currency_wording_wins_over_the_iso_fallback():
    """uk+UAH is implemented, so it must keep its declined unit name."""
    assert spell_total(Decimal("2"), money(), "uk").startswith("Дві гривні")


def test_spell_total_returns_empty_for_unsupported_language():
    """Neither path can spell an unknown language."""
    assert spell_total(Decimal("2"), money(), "zz") == ""
