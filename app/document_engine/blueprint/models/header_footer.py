from app.document_engine.blueprint.models.blueprint_base import BlueprintBase
from app.document_engine.blueprint.models.unions import BlueprintBlock

from app.document_engine.enums.enums import HeaderFooterType


class HeaderFooterBlueprint(BlueprintBase):
    type: HeaderFooterType
    blocks: tuple[BlueprintBlock, ...]


class HeaderFooterGroupBlueprint(BlueprintBase):
    default: HeaderFooterBlueprint | None
    first: HeaderFooterBlueprint | None
    even: HeaderFooterBlueprint | None