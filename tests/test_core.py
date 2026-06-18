"""Tests for the cross-cutting error / diagnostics foundation in app.core."""

from app.core.diagnostics import Diagnostic, DiagnosticCollector
from app.core.errors import Layer, Severity, ErrorCategory
from app.document_engine.parser.errors import ParserFormatError, UnsupportedFeatureError


def test_app_error_carries_metadata():
    err = ParserFormatError("boom", context={"part": "document.xml"})
    assert err.layer is Layer.PARSER
    assert err.category is ErrorCategory.FORMAT
    assert err.code == "ParserFormatError"          # defaults to class name
    assert err.context == {"part": "document.xml"}
    assert err.user_message is None


def test_as_diagnostic_uses_str_when_no_user_message():
    err = ParserFormatError("malformed body")
    diag = err.as_diagnostic()
    assert diag.severity is Severity.ERROR          # default
    assert diag.layer is Layer.PARSER
    assert diag.code == "ParserFormatError"
    assert diag.message == "malformed body"


def test_as_diagnostic_prefers_user_message_and_severity():
    err = ParserFormatError("internal detail", user_message="The file is corrupt.")
    diag = err.as_diagnostic(Severity.WARNING)
    assert diag.severity is Severity.WARNING
    assert diag.message == "The file is corrupt."


def test_recoverable_defaults_false_but_set_on_unsupported():
    assert ParserFormatError("x").recoverable is False
    assert UnsupportedFeatureError("x").recoverable is True


def test_collector_warn_appends_warning():
    collector = DiagnosticCollector()
    collector.warn(Layer.BLUEPRINT, "bad_key", "Unknown key", key="nope")

    assert len(collector.items) == 1
    diag = collector.items[0]
    assert diag.severity is Severity.WARNING
    assert diag.layer is Layer.BLUEPRINT
    assert diag.code == "bad_key"
    assert diag.context == {"key": "nope"}


def test_collector_warnings_and_has_errors():
    collector = DiagnosticCollector()
    collector.warn(Layer.PARSER, "w", "a warning")
    collector.record(
        Diagnostic(Layer.PARSER, Severity.ERROR, "e", "an error")
    )

    assert len(collector.warnings) == 1
    assert collector.warnings[0].code == "w"
    assert collector.has_errors is True


def test_collector_empty_has_no_errors():
    collector = DiagnosticCollector()
    assert collector.warnings == []
    assert collector.has_errors is False
