"""Blueprint serialization, template persistence, asset GC and the import service."""

import json

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.assets.provider import DbAssetProvider
from app.assets.service import AssetBlob
from app.db.associations import template_asset_m2m
from app.db.models.core.assets import Asset
from app.db.models.core.template import Template
from app.document_engine.blueprint.assets import collect_assets_ids
from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint
from app.document_engine.blueprint.models.segment import (
    ImageSegment, PlaceholderSegment, TextSegment,
)
from app.document_engine.blueprint.models.template import TemplateBlueprint, TemplateConfig
from app.document_engine.blueprint.serialize import dump_blueprint, load_blueprint
from app.document_engine.enums.enums import PlaceholderType
from app.document_engine.orchestration.pipeline import TemplateIngestionPipeline
from app.services.errors import EntityNotFound
from app.services.template.db_input_provider import DbTemplateInputProvider
from app.services.template.import_service import TemplateImportService
from app.services.template.repository import TemplateRepository


@pytest.fixture
def blueprint(make_docx, make_png, fixture_provider) -> TemplateBlueprint:
    """A blueprint built from a real .docx containing text, placeholders, a table and an image."""
    path = make_docx(
        paragraphs=["Invoice for {{ org_name }}", "No. {{ invoice_no.UKR }}"],
        table=[["Item", "Total"]],
        image=make_png(),
    )
    pipeline = TemplateIngestionPipeline(fixture_provider)
    result = pipeline.ingest(path)
    return pipeline.finalize(result.draft)


@pytest.fixture
def ingested(make_docx, make_png, fixture_provider):
    """(blueprint, asset bundle) from a template that embeds one image."""
    path = make_docx(paragraphs=["Invoice for {{ org_name }}"], image=make_png())
    pipeline = TemplateIngestionPipeline(fixture_provider)
    result = pipeline.ingest(path)
    return pipeline.finalize(result.draft), result.assets


def segments_of(bp: TemplateBlueprint) -> list:
    out = []
    for section in bp.sections:
        for block in section.blocks:
            if isinstance(block, ParagraphBlueprint):
                out.extend(block.segments)
    return out


# --- serialization -----------------------------------------------------------

def test_dump_produces_json_serializable_structures(blueprint):
    """mode='json' must flatten enums; otherwise the JSON column write fails."""
    sections, placeholders, config = dump_blueprint(blueprint)

    json.dumps(sections)
    json.dumps(placeholders)
    json.dumps(config)


def test_blueprint_survives_a_dump_load_round_trip(blueprint):
    restored = load_blueprint(*dump_blueprint(blueprint))

    assert restored == blueprint


def test_round_trip_preserves_discriminated_segment_types(blueprint):
    """The riskiest part: unions must rebuild as their concrete classes, not dicts."""
    restored = load_blueprint(*dump_blueprint(blueprint))

    original = [type(s) for s in segments_of(blueprint)]
    rebuilt = [type(s) for s in segments_of(restored)]

    assert rebuilt == original
    assert PlaceholderSegment in rebuilt
    assert ImageSegment in rebuilt
    assert TextSegment in rebuilt


def test_round_trip_preserves_placeholder_language_and_type(blueprint):
    restored = load_blueprint(*dump_blueprint(blueprint))

    by_key = {
        s.key: s for s in segments_of(restored) if isinstance(s, PlaceholderSegment)
    }
    assert by_key["invoice_no"].language == "UKR"
    assert by_key["org_name"].language == "ENG"          # default language
    assert by_key["org_name"].ph_type is PlaceholderType.SCALAR


def test_round_trip_preserves_image_asset_id_and_size(blueprint):
    restored = load_blueprint(*dump_blueprint(blueprint))

    original = [s for s in segments_of(blueprint) if isinstance(s, ImageSegment)][0]
    rebuilt = [s for s in segments_of(restored) if isinstance(s, ImageSegment)][0]

    assert rebuilt.asset_id == original.asset_id
    assert (rebuilt.width_emu, rebuilt.height_emu) == (original.width_emu, original.height_emu)


def test_round_trip_preserves_config_and_placeholder_definitions(blueprint):
    restored = load_blueprint(*dump_blueprint(blueprint))

    assert restored.config == blueprint.config
    assert restored.placeholders == blueprint.placeholders


# --- repository: save / get --------------------------------------------------

def test_save_returns_id_and_writes_queryable_columns(session: Session, ingested):
    bp, bundle = ingested

    template_id = TemplateRepository(session).save(bp, bundle)

    row = session.get(Template, template_id)
    assert row.name == bp.config.name
    assert row.type == bp.config.type
    assert row.created_at is not None


def test_saved_blueprint_round_trips_through_the_database(session: Session, ingested):
    bp, bundle = ingested
    repo = TemplateRepository(session)

    template_id = repo.save(bp, bundle)
    session.expunge_all()                       # force a real reload, not identity-map cache

    assert repo.get(template_id) == bp


def test_save_persists_referenced_asset_blobs(session: Session, ingested):
    bp, bundle = ingested
    (sha,) = collect_assets_ids(bp)

    TemplateRepository(session).save(bp, bundle)

    stored = session.get(Asset, sha)
    assert stored.data == bundle[sha].data
    assert stored.mime_type == "image/png"
    assert stored.size_bytes == len(bundle[sha].data)


def test_save_links_template_to_its_assets(session: Session, ingested):
    bp, bundle = ingested

    template_id = TemplateRepository(session).save(bp, bundle)

    links = session.execute(
        select(template_asset_m2m.c.asset_sha256)
        .where(template_asset_m2m.c.template_id == template_id)
    ).scalars().all()
    assert set(links) == collect_assets_ids(bp)


def test_save_ignores_bundle_entries_the_blueprint_does_not_reference(session: Session, ingested):
    """A parsed-but-dropped image must not leave an orphan BLOB behind."""
    bp, bundle = ingested
    padded = dict(bundle) | {
        "deadbeef": AssetBlob(sha256="deadbeef", mime_type="image/png", data=b"unused"),
    }

    TemplateRepository(session).save(bp, padded)

    assert session.get(Asset, "deadbeef") is None
    assert len(session.scalars(select(Asset)).all()) == 1


def test_saving_two_templates_with_the_same_image_stores_one_blob(session: Session, ingested):
    bp, bundle = ingested
    repo = TemplateRepository(session)

    repo.save(bp, bundle)
    repo.save(bp, bundle)

    assert len(session.scalars(select(Asset)).all()) == 1
    assert len(session.scalars(select(Template)).all()) == 2


def test_get_raises_for_unknown_template(session: Session):
    with pytest.raises(EntityNotFound):
        TemplateRepository(session).get(9999)


# --- repository: delete + asset GC -------------------------------------------

def test_delete_removes_the_template_and_its_links(session: Session, ingested):
    bp, bundle = ingested
    repo = TemplateRepository(session)
    template_id = repo.save(bp, bundle)

    repo.delete(template_id)

    assert session.get(Template, template_id) is None
    assert session.execute(select(template_asset_m2m)).all() == []


def test_delete_collects_the_now_orphaned_asset(session: Session, ingested):
    bp, bundle = ingested
    repo = TemplateRepository(session)
    template_id = repo.save(bp, bundle)

    repo.delete(template_id)

    assert session.scalars(select(Asset)).all() == []


def test_shared_asset_survives_until_its_last_template_is_deleted(session: Session, ingested):
    """The reference-counting rule: an asset dies only with its final referent."""
    bp, bundle = ingested
    repo = TemplateRepository(session)
    first, second = repo.save(bp, bundle), repo.save(bp, bundle)
    (sha,) = collect_assets_ids(bp)

    repo.delete(first)
    assert session.get(Asset, sha) is not None, "still referenced by the second template"

    repo.delete(second)
    assert session.get(Asset, sha) is None, "last reference gone -> collected"


def test_delete_raises_for_unknown_template(session: Session):
    with pytest.raises(EntityNotFound):
        TemplateRepository(session).delete(9999)


# --- asset provider (render side) --------------------------------------------

def test_db_asset_provider_reads_back_a_saved_blob(session: Session, ingested):
    bp, bundle = ingested
    TemplateRepository(session).save(bp, bundle)
    (sha,) = collect_assets_ids(bp)

    asset = DbAssetProvider(session).get(sha)

    assert asset.data == bundle[sha].data
    assert asset.mime == "image/png"


def test_db_asset_provider_returns_none_for_unknown_asset(session: Session):
    assert DbAssetProvider(session).get("nope") is None


# --- DbTemplateInputProvider -------------------------------------------------

def test_input_provider_maps_the_default_config_row(session: Session, seeded_inputs):
    config = DbTemplateInputProvider(session).default_template_config()

    assert config.primary_language == "ENG"
    assert config.secondary_language == "UKR"
    assert config.type == "invoice"
    assert config.name == "Default invoice"
    assert config.append_currency is True


def test_input_provider_derives_languages_from_the_config(session: Session, seeded_inputs):
    assert DbTemplateInputProvider(session).languages() == {"ENG", "UKR"}


def test_input_provider_prefers_an_injected_config(session: Session, seeded_inputs):
    """The GUI picks languages before import; the injected config must win over the DB row."""
    injected = TemplateConfig(
        primary_language="UKR", secondary_language=None,
        type="act", name="chosen", description="", append_currency=False,
    )
    provider = DbTemplateInputProvider(session, config=injected)

    assert provider.default_template_config() is injected
    assert provider.languages() == {"UKR"}


def test_input_provider_raises_when_defaults_are_missing(session: Session):
    with pytest.raises(EntityNotFound):
        DbTemplateInputProvider(session).default_template_config()


def test_placeholder_defaults_expose_the_keys_the_builder_needs(session: Session, seeded_inputs):
    defaults = DbTemplateInputProvider(session).placeholder_defaults()

    assert defaults["org_name"] == {
        "active": True, "required": True, "type": PlaceholderType.SCALAR,
    }


def test_placeholder_defaults_include_inactive_rows(session: Session, seeded_inputs):
    """Kept so the builder can say 'disabled' rather than 'unknown key'."""
    defaults = DbTemplateInputProvider(session).placeholder_defaults()

    assert defaults["retired_key"]["active"] is False


def test_disabled_placeholder_is_rejected_at_ingestion(session, seeded_inputs, make_docx):
    path = make_docx(paragraphs=["Hello {{ retired_key }}"])
    pipeline = TemplateIngestionPipeline(DbTemplateInputProvider(session))

    result = pipeline.ingest(path)

    assert len(result.diagnostics.warnings) == 1
    assert "retired_key" not in result.draft.context.placeholders


# --- import service ----------------------------------------------------------

def test_ingest_does_not_touch_the_database(session: Session, seeded_inputs,
                                            make_docx, make_png):
    path = make_docx(paragraphs=["Invoice for {{ org_name }}"], image=make_png())
    service = TemplateImportService(session, DbTemplateInputProvider(session))

    service.ingest(path)

    assert session.scalars(select(Template)).all() == []
    assert session.scalars(select(Asset)).all() == []


def test_commit_persists_the_reviewed_draft(session: Session, seeded_inputs,
                                            make_docx, make_png):
    path = make_docx(paragraphs=["Invoice for {{ org_name }}"], image=make_png())
    service = TemplateImportService(session, DbTemplateInputProvider(session))

    result = service.ingest(path)
    template_id = service.commit(result)

    assert session.get(Template, template_id) is not None
    assert len(session.scalars(select(Asset)).all()) == 1
    assert "org_name" in TemplateRepository(session).get(template_id).placeholders
