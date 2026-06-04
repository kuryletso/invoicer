from app.document_engine.blueprint.models.blueprint_base import BlueprintBase

class MarginsBlueprint(BlueprintBase):
    top: int            # twips
    bottom: int         # twips
    left: int           # twips
    right: int          # twips