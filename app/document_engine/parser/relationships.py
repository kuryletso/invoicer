from dataclasses import dataclass
from pathlib import PurePosixPath

from lxml.etree import _Element

from app.document_engine.parser.namespaces import NS

PACKAGE_ROOT = PurePosixPath("word")


@dataclass(slots=True)
class Relationship:
    id: str
    type: str
    target: str
    is_external: bool


class RelationshipResolver:
    def __init__(self, relationships_root: _Element) -> None:
        self._relationships: dict[str, Relationship] = {}

        for relationship in relationships_root.findall("pr:Relationship", NS):
            relationship_id = relationship.get("Id")
            relationship_type = relationship.get("Type")
            target = relationship.get("Target")

            if relationship_id is None \
            or relationship_type is None \
            or target is None:
                continue

            target_mode = relationship.get("TargetMode")
            is_external = target_mode == "External"

            normalized_target = (
                target
                if is_external
                else self._normalize_target(target)
            )

            self._relationships[relationship_id] = Relationship(
                id=relationship_id,
                type=relationship_type,
                target=normalized_target,
                is_external=is_external,
            )

    def get(self, relationship_id: str) -> Relationship | None:
        return self._relationships.get(relationship_id)
    
    def resolve(self, relationship_id: str) -> str | None:
        relationship = self.get(relationship_id)
        if relationship is None:
            return None
        
        return relationship.target
    
    @staticmethod
    def _normalize_target(target: str) -> str:
        normalized = PACKAGE_ROOT / PurePosixPath(target)
        return str(normalized)