from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.document_engine.rendering.context import Values
from app.services.money import MoneyFormat


@dataclass(slots=True, frozen=True)
class Representative:
    name: Values
    title: Values | None


@dataclass(slots=True, frozen=True)
class TaxId:
    value: str
    system: Values
    country: Values


@dataclass(slots=True, frozen=True)
class BankDetails:
    iban: str
    swift: str | None
    bank_name: Values
    bank_info: Values


@dataclass(slots=True, frozen=True)
class Party:
    legal_name: Values
    address: Values
    org_type: Values
    tax_id: TaxId
    email: str | None
    phone: str | None
    representative: Representative | None
    bank: BankDetails | None


@dataclass(slots=True, frozen=True)
class Line:
    description: Values
    unit: Values
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal


@dataclass(slots=True, frozen=True)
class InvoiceData:
    prefix: str
    number: int
    issue_date: date
    currency: MoneyFormat
    provider: Party
    client: Party
    lines: tuple[Line, ...]