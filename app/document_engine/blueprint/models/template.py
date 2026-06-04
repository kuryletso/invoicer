from app.document_engine.blueprint.models.blueprint_base import BlueprintBase
from app.document_engine.blueprint.models.section import SectionBlueprint


class PlaceholderDefinition(BlueprintBase):
    required: bool = False


class TemplateBlueprint(BlueprintBase):
    sections: tuple[SectionBlueprint, ...]
    placeholders: dict[str, PlaceholderDefinition]