import sys

from app.document_engine.blueprint.models.template import TemplateBlueprint
from app.document_engine.blueprint.models.section import SectionBlueprint
from app.document_engine.blueprint.models.header_footer import (
    HeaderFooterBlueprint,
    HeaderFooterGroupBlueprint,
)
from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint
from app.document_engine.blueprint.models.table import (
    TableBlueprint,
    TablePlaceholder,
    RowBlueprint,
    RowPlaceholder,
    CellBlueprint,
    CellPlaceholder,
)
from app.document_engine.blueprint.models.segment import (
    TextSegment,
    PlaceholderSegment,
    JoinedPlaceholderSegment,
    GroupedPlaceholderSegment,
    ImageSegment,
)
from app.document_engine.blueprint.models.unions import (
    BlueprintSegment,
    BlueprintCell,
    BlueprintRow,
    BlueprintBlock,
)

_ALIASES = {
    "BlueprintSegment": BlueprintSegment,
    "BlueprintCell": BlueprintCell,
    "BlueprintRow": BlueprintRow,
    "BlueprintBlock": BlueprintBlock,
}

# (!) Must be in sync with whichever model modules carry TYPE_CHECKING-only union refs
_ALIAS_MODULES = (
    "app.document_engine.blueprint.models.section",
    "app.document_engine.blueprint.models.header_footer",
    "app.document_engine.blueprint.models.paragraph",
    "app.document_engine.blueprint.models.table",
)


def rebuild_models():
    for module_name in _ALIAS_MODULES:
        vars(sys.modules[module_name]).update(_ALIASES)

    models = [
        TemplateBlueprint,
        SectionBlueprint,
        HeaderFooterGroupBlueprint,
        HeaderFooterBlueprint,
        ParagraphBlueprint,
        TableBlueprint,
        TablePlaceholder,
        RowBlueprint,
        RowPlaceholder,
        CellBlueprint,
        CellPlaceholder,
        TextSegment,
        PlaceholderSegment,
        JoinedPlaceholderSegment,
        GroupedPlaceholderSegment,
        ImageSegment,
    ]

    for model in models:
        model.model_rebuild()
