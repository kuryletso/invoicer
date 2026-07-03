"""End-to-end tests for the template ingestion pipeline."""

import zipfile

import pytest

from app.core.errors import Layer
from app.document_engine.orchestration.pipeline import TemplateIngestionPipeline
from app.document_engine.orchestration.results import IngestionResult
from app.document_engine.orchestration.errors import IngestionError
from app.document_engine.blueprint.models.template import TemplateBlueprint
from app.document_engine.parser.errors import ParserError


def test_ingest_returns_draft_and_registers_placeholders(make_docx, fixture_provider):
    path = make_docx(
        paragraphs=["Invoice for {{ org_name }}", "Number {{ invoice_no }}"],
        table=[["Item", "Total"]],
    )
    pipeline = TemplateIngestionPipeline(fixture_provider)

    result = pipeline.ingest(path)

    assert isinstance(result, IngestionResult)
    assert len(result.draft.sections) == 1
    assert {"org_name", "invoice_no"} <= set(result.draft.context.placeholders)
    assert result.diagnostics.warnings == []


def test_ingest_surfaces_warning_for_unknown_placeholder(make_docx, fixture_provider):
    path = make_docx(paragraphs=["Hello {{ unknown_key }}"])
    pipeline = TemplateIngestionPipeline(fixture_provider)

    result = pipeline.ingest(path)

    assert len(result.diagnostics.warnings) == 1
    assert result.diagnostics.warnings[0].layer is Layer.BLUEPRINT
    assert "unknown_key" not in result.draft.context.placeholders


def test_finalize_produces_blueprint(make_docx, fixture_provider):
    path = make_docx(paragraphs=["Invoice for {{ org_name }}"])
    pipeline = TemplateIngestionPipeline(fixture_provider)

    result = pipeline.ingest(path)
    blueprint = pipeline.finalize(result.draft)

    assert isinstance(blueprint, TemplateBlueprint)
    assert "org_name" in blueprint.placeholders


def test_ingest_wraps_stage_failure_in_ingestion_error(tmp_path, fixture_provider):
    bogus = tmp_path / "bogus.docx"
    with zipfile.ZipFile(bogus, "w") as zf:
        zf.writestr("not-a-docx.txt", "hello")

    pipeline = TemplateIngestionPipeline(fixture_provider)

    with pytest.raises(IngestionError) as excinfo:
        pipeline.ingest(bogus)

    # original parser failure is attached as the cause, attributed to orchestration
    assert excinfo.value.layer is Layer.ORCHESTRATION
    assert isinstance(excinfo.value.__cause__, ParserError)


def test_fixture_provider_satisfies_input_protocol(fixture_provider):
    assert isinstance(fixture_provider.languages(), set)
    assert isinstance(fixture_provider.placeholder_defaults(), dict)
    assert fixture_provider.default_template_config().primary_language == "ENG"
