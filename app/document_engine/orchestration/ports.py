from typing import Any, Protocol

from app.document_engine.blueprint.models.template import TemplateConfig


class TemplateInputProvider(Protocol):
    def placeholder_defaults(self) -> dict[str, dict[str, Any]]:
        ...

    def languages(self) -> set[str]:
        ...

    def default_template_config(self) -> TemplateConfig:
        ...