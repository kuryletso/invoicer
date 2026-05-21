from pydantic import BaseModel, ConfigDict

class BlueprintNode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )