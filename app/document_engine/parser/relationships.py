from lxml.etree import _Element


class RelationshipResolver:
    def __init__(self, relationships_root: _Element) -> None:
        self.relationships: dict[str, str] = {}

        for relationship in relationships_root:
            relationship_id = relationship.get("Id")
            target = relationship.get("Target")

            if relationship_id is None:
                continue
            if target is None:
                continue

            self.relationships[relationship_id] = target

    def resolve(self, relationship_id: str) -> str | None:
        return self.relationships.get(relationship_id)