from sqlalchemy import Enum as SQLEnum

from app.domain.enums import Language, Currency, DocumentType, MeasurementUnit, Country, TaxIdSystem

LanguageEnum = SQLEnum(
    Language,
    name="language_enum"
)

CurrencyEnum = SQLEnum(
    Currency,
    name="currency_enum"
)

DocumentTypeEnum = SQLEnum(
    DocumentType,
    name="document_type_enum"
)

MeasurementUnitEnum = SQLEnum(
    MeasurementUnit,
    name="measurement_unit_enum"
)

CountryEnum = SQLEnum(
    Country,
    name="country_enum"
)

TaxIdSystemEnum = SQLEnum(
    TaxIdSystem,
    name="tax_id_system_enum"
)