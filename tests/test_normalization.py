"""Tests for the structural normalizer (normalize stage)."""

import pytest

from app.core.diagnostics import DiagnosticCollector
from app.document_engine.parser.parser import DocxParser
from app.document_engine.parser.models.blocks import SectionBreakNode
from app.document_engine.normalization.structural_normalizer import StructuralNormalizer
from app.document_engine.normalization.models.blocks import (
    NormalizedParagraph,
    NormalizedTable,
)
from app.document_engine.normalization.errors import NormalizationFormatError


def _parse(path) -> list:
    with DocxParser(path, diagnostics=DiagnosticCollector()) as parser:
        return parser.parse()


def test_normalize_groups_blocks_into_section(make_docx):
    parsed = _parse(make_docx(paragraphs=["one", "two"], table=[["A", "B"]]))

    sections = StructuralNormalizer.normalize(parsed, DiagnosticCollector())

    assert len(sections) == 1
    block_kinds = [type(b).__name__ for b in sections[0].blocks]
    assert block_kinds == ["NormalizedParagraph", "NormalizedParagraph", "NormalizedTable"]
    assert isinstance(sections[0].blocks[0], NormalizedParagraph)
    assert isinstance(sections[0].blocks[-1], NormalizedTable)


def test_normalize_empty_list_raises():
    with pytest.raises(NormalizationFormatError):
        StructuralNormalizer.normalize([], DiagnosticCollector())


def test_normalize_invalid_block_type_raises():
    with pytest.raises(NormalizationFormatError):
        StructuralNormalizer.normalize([object()], DiagnosticCollector())


def test_normalize_without_trailing_section_break_raises(make_docx):
    parsed = _parse(make_docx(paragraphs=["dangling"]))
    # Drop the trailing section break so blocks have no section to close into.
    assert isinstance(parsed[-1], SectionBreakNode)
    truncated = parsed[:-1]

    with pytest.raises(NormalizationFormatError):
        StructuralNormalizer.normalize(truncated, DiagnosticCollector())
