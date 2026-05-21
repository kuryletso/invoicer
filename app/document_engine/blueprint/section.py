from pydantic import BaseModel

from app.document_engine.blueprint.unions import Block

class SectionBlueprint(BaseModel):
    page_width: int
    page_height: int
    margin_top: int
    margin_bottom: int

    blocks: list[Block]