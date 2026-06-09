#
# DEPRECATED
# 

from enum import StrEnum


class _Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    UAH = "UAH"


class _Language(StrEnum):
    ENG = "en"
    UKR = "uk"


class _MeasurementUnit(StrEnum):
    ...


class _Country(StrEnum):
    UKR = "ukr"
    USA = "usa"


class _TaxIdSystem(StrEnum):
    VAT = "vat"
    EIN = "ein"
    EDRPOU = "edrpou"
    SSN = "ssn"


class _DocumentType(StrEnum):
    INVOICE = "invoice"
    ACT = "act"
    QUOTE = "quote"
    CONTRACT = "contract"