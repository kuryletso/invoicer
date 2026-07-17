from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

SEED_DIR = Path(__file__).parent / "seed_data"


@dataclass(frozen=True)
class SeedSpec:
    filename: str
    model: type
    transform: Callable[[dict], dict] | None = None     # raw json row -> column dict


def _upsert(
        session: Session,
        model,
        rows: list[dict],
) -> None:
    
    if not rows:
        return
    
    pk = [ c.name for c in model.__table__.primary_key ]
    stmt = insert(model).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=pk,
        set_={ c: stmt.excluded[c] for c in rows[0] if c not in pk },
    )
    session.execute(stmt)


def seed(
        session: Session,
        specs: tuple[SeedSpec, ...],
) -> None:
    
    for spec in specs:
        raw = json.loads((SEED_DIR / spec.filename).read_text(encoding="UTF-8"))
        rows = [ spec.transform(r) for r in raw ] if spec.transform else raw
        _upsert(session, spec.model, rows)

    session.commit()


def _language_row(raw: dict) -> dict:
    return {
        "code": raw["ISO 649-3"].upper(),
        "code_alpha_2": raw["ISO 649-1"],
        "label_en": raw["ISO language name"],
        "label_uk": raw["Ukrainian"],
    }