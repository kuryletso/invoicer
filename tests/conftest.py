from typing import Any, Callable
from pathlib import Path

import pytest
from docx import Document

from app.core.diagnostics import DiagnosticCollector
from app.document_engine.blueprint.models.template import TemplateConfig
from app.document_engine.blueprint.template_builder import TemplateBuilderContext
from app.document_engine.normalization.models.inlines import (
    NormalizedTextNode,
    NormalizedTextStyle,
)


class FixtureInputProvider:
    """In-memory TemplateInputProvider for tests/dev — no database required.

    Structurally satisfies orchestration.ports.TemplateInputProvider.
    """

    def __init__(
        self,
        *,
        languages: set[str] | None = None,
        placeholders: dict[str, dict[str, Any]] | None = None,
        config: TemplateConfig | None = None,
    ) -> None:
        self._languages = languages or {"en", "uk"}
        self._placeholders = placeholders or {
            "org_name": {"active": True, "required": True},
            "invoice_no": {"active": True, "required": True},
        }
        self._config = config or TemplateConfig(
            primary_language="en",
            secondary_language=None,
            type="invoice",
            name="seed",
            description="",
        )

    def default_template_config(self) -> TemplateConfig:
        return self._config

    def placeholder_defaults(self) -> dict[str, dict[str, Any]]:
        return self._placeholders

    def languages(self) -> set[str]:
        return self._languages


@pytest.fixture
def fixture_provider() -> FixtureInputProvider:
    return FixtureInputProvider()


@pytest.fixture
def diagnostics() -> DiagnosticCollector:
    return DiagnosticCollector()


@pytest.fixture
def make_docx(tmp_path: Path) -> Callable[..., Path]:
    """Factory building a real .docx via python-docx into the test's tmp dir."""

    def _make(
        paragraphs: list[str] | tuple[str, ...] = (),
        table: list[list[str]] | None = None,
        name: str = "test.docx",
    ) -> Path:
        document = Document()
        for text in paragraphs:
            document.add_paragraph(text)

        if table:
            rows, cols = len(table), len(table[0])
            built = document.add_table(rows=rows, cols=cols)
            for r, row in enumerate(table):
                for c, value in enumerate(row):
                    built.cell(r, c).text = value

        path = tmp_path / name
        document.save(path)
        return path

    return _make


@pytest.fixture
def make_text_node() -> Callable[[str], NormalizedTextNode]:
    def _make(text: str) -> NormalizedTextNode:
        return NormalizedTextNode(
            text=text,
            style=NormalizedTextStyle(
                bold=False,
                italic=False,
                underline=False,
                font_name="Calibri",
                font_size=22,
                color="000000",
            ),
        )

    return _make


@pytest.fixture
def make_context() -> Callable[..., TemplateBuilderContext]:
    """Factory for a TemplateBuilderContext with its own DiagnosticCollector.

    Inspect emitted warnings afterwards via ``context.diagnostics.warnings``.
    """

    def _make(
        *,
        default_language: str = "en",
        languages: set[str] | None = None,
        placeholders: dict[str, dict[str, Any]] | None = None,
        diagnostics: DiagnosticCollector | None = None,
    ) -> TemplateBuilderContext:
        return TemplateBuilderContext(
            default_language=default_language,
            placeholder_defaults=placeholders
            or {
                "org_name": {"active": True, "required": True},
                "invoice_no": {"active": True, "required": True},
            },
            languages=languages or {"en", "uk"},
            placeholders={},
            diagnostics=diagnostics or DiagnosticCollector(),
        )

    return _make
