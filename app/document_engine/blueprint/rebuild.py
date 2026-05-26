from app.document_engine.blueprint.document import DocumentBlueprint
from app.document_engine.blueprint.section import SectionBlueprint
from app.document_engine.blueprint.paragraph import ParagraphBlueprint
from app.document_engine.blueprint.table import TableBlueprint, RowBlueprint, CellBlueprint
from app.document_engine.blueprint.segment import TextSegment, PlaceholderSegment, ImageSegment


def rebuild_models():
    models = [
        DocumentBlueprint,
        SectionBlueprint,
        ParagraphBlueprint,
        TableBlueprint,
        RowBlueprint,
        CellBlueprint,
        TextSegment,
        PlaceholderSegment,
        ImageSegment,
    ]

    for model in models:
        model.model_rebuild()