from pydantic import BaseModel, ConfigDict


class BlueprintBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )