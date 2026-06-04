from app.document_engine.blueprint.models.template import TemplateBlueprint
from app.document_engine.blueprint.models.section import SectionBlueprint
from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint
from app.document_engine.blueprint.models.table import TableBlueprint, RowBlueprint, CellBlueprint
from app.document_engine.blueprint.models.segment import (
    TextSegment,
    PlaceholderSegment,
    JoinedPlaceholderSegment,
    GroupedPlaceholderSegment,
    ImageSegment,
)


def rebuild_models():
    models = [
        TemplateBlueprint,
        SectionBlueprint,
        ParagraphBlueprint,
        TableBlueprint,
        RowBlueprint,
        CellBlueprint,
        TextSegment,
        PlaceholderSegment,
        JoinedPlaceholderSegment,
        GroupedPlaceholderSegment,
        ImageSegment,
    ]

    for model in models:
        model.model_rebuild()