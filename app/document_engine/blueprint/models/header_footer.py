from __future__ import annotations

from typing import TYPE_CHECKING

from app.document_engine.blueprint.models.blueprint_base import BlueprintBase

from app.document_engine.enums.enums import HeaderFooterType

if TYPE_CHECKING:
    from app.document_engine.blueprint.models.unions import BlueprintBlock


class HeaderFooterBlueprint(BlueprintBase):
    type: HeaderFooterType
    blocks: tuple[BlueprintBlock, ...]


class HeaderFooterGroupBlueprint(BlueprintBase):
    default: HeaderFooterBlueprint | None
    first: HeaderFooterBlueprint | None
    even: HeaderFooterBlueprint | None