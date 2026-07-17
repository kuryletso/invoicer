from app.db.seed import SeedSpec, _language_row
from app.db.models.references.language import Language
from app.db.models.registries.placeholder import PlaceholderRegistry


SEED_SPECS: tuple[SeedSpec, ...] = (
    SeedSpec("ISO Languages.json", Language, _language_row),
    SeedSpec("placeholder.json", PlaceholderRegistry),
)