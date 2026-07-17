from __future__ import annotations

from typing import Final

# template level
DATE: Final = "date"
PREFIX: Final = "prefix"
ID: Final = "id"
SUBTOTAL: Final = "subtotal"
TOTAL_TAX: Final = "total_tax"
TOTAL: Final = "total"
TOTAL_TEXT: Final = "total_text"
CURRENCY: Final = "curr"

# party roles
CLIENT: Final = "client"
PROVIDER: Final = "provider"

# party fields
NAME: Final = "name"
REP_NAME: Final = "rep_name"
REP_TITLE: Final = "rep_title"
TYPE: Final = "type"
TAX_ID: Final = "tax_id"
TAX_SYS: Final = "tax_sys"
COUNTRY: Final = "country"
ADDRESS: Final = "address"
PHONE: Final = "phone"
EMAIL: Final = "email"
IBAN: Final = "iban"
SWIFT: Final = "swift"
BANK_NAME: Final = "bank_name"
BANK_INFO: Final = "bank_info"


def party_key(role: str, field: str) -> str:
    return f"{role}_{field}"