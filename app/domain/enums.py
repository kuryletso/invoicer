from enum import StrEnum

class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    UAH = "UAH"

class Language(StrEnum):
    ENG = "en"
    UKR = "uk"


class MeasurenentUnit(StrEnum):
    ...


class Country(StrEnum):
    UKR = "ukr"
    USA = "usa"

class TaxIdSystem(StrEnum):
    VAT = "vat"
    EIN = "ein"
    EDRPOU = "edrpou"
    SSN = "ssn"