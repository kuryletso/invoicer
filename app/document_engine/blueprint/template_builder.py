from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

from app.core.diagnostics import DiagnosticCollector

from app.document_engine.blueprint.models.template import TemplateBlueprint, PlaceholderDefinition, TemplateConfig
from app.document_engine.blueprint.models.section import SectionBlueprint
from app.document_engine.blueprint.errors import PlaceholderSyntaxError

from app.document_engine.normalization.models.sections import NormalizedSection

if TYPE_CHECKING:
    from app.document_engine.blueprint.builders.section import section_bp_from_normalized



@dataclass(slots=True)
class TemplateDraftConfig:
    primary_language: str
    type: str
    name: str
    secondary_language: str | None = None
    description: str = ""

    @classmethod
    def from_template_config(
        cls,
        config: TemplateConfig,
    ) -> TemplateDraftConfig:
        
        return TemplateDraftConfig(
            primary_language=config.primary_language,
            secondary_language=config.secondary_language,
            type=config.type,
            name=config.name,
            description=config.description,
        )

    def to_template_config(self) -> TemplateConfig:
        return TemplateConfig(
            primary_language=self.primary_language,
            secondary_language=self.secondary_language,
            type=self.type,
            name=self.name,
            description=self.description,
        )

@dataclass(slots=True)
class TemplateBuilderContext:
    default_language: str
    placeholder_defaults: dict[str, dict[str, Any]]
    languages: set[str]
    placeholders: dict[str, dict]
    diagnostics: DiagnosticCollector


    def register_placeholder(
        self,
        key: str,
    ) -> None:
        
        if key in self.placeholder_defaults:
            if not self.placeholder_defaults[key].get("active", False):
                raise PlaceholderSyntaxError(
                    f"Placeholder key '{key}' is disabled."
                )

            self.placeholders.setdefault(key, self.placeholder_defaults[key])

        else:
            raise PlaceholderSyntaxError(
                f"Not registered key in placeholder: {key}."
            )
        

@dataclass(slots=True)
class TemplateDraft:
    sections: list[SectionBlueprint]
    context: TemplateBuilderContext
    config: TemplateDraftConfig


class TemplateBuilder:

    def build_draft(
        self,
        normalized: tuple[NormalizedSection, ...],
        default_config: TemplateConfig,
        placeholder_defaults: dict[str, dict[str, Any]],      # request from placeholders registry table
        languages: set[str],        # request from languages reference table
        diagnostics: DiagnosticCollector,
    ) -> TemplateDraft:

        config = TemplateDraftConfig.from_template_config(default_config)

        context = TemplateBuilderContext(
            default_language=config.primary_language,
            placeholder_defaults=placeholder_defaults,
            languages=languages,
            placeholders={},
            diagnostics=diagnostics,
        )

        sections = [
            section_bp_from_normalized(section, context)
            for section in normalized
        ]

        return TemplateDraft(
            sections=sections,
            context=context,
            config=config,
        )

    def _define_placeholders(
        self,
        placeholders: dict[str, dict],
    ) -> dict[str, PlaceholderDefinition]:
        
        return {
            k: PlaceholderDefinition(required=v.get("required", True))
            for k,v in placeholders.items()
        }
    

    def save_draft(
        self,
        draft: TemplateDraft,
    ) -> TemplateBlueprint:
        
        return TemplateBlueprint(
            sections=tuple(draft.sections),
            placeholders=self._define_placeholders(draft.context.placeholders),
            config=draft.config.to_template_config(),
        )