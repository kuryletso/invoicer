from pydantic import BaseModel

from app.document_engine.blueprint.section import SectionBlueprint

class DocumentBlueprint(BaseModel):
    sections: list[SectionBlueprint]