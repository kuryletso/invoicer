from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LanguageSpec:
    code: str       # ISO-639-3, "ENG", "UKR"
    alpha_2: str    # ISO 639-1 for num2word, "en", "uk"