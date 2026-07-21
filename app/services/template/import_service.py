from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.document_engine.orchestration.pipeline import TemplateIngestionPipeline
from app.document_engine.orchestration.ports import TemplateInputProvider
from app.document_engine.orchestration.results import IngestionResult
from app.services.template.repository import TemplateRepository


class TemplateImportService:

    def __init__(
            self,
            session: Session,
            inputs: TemplateInputProvider,
    ) -> None:
        
        self._pipeline = TemplateIngestionPipeline(inputs)
        self._repo = TemplateRepository(session)


    def ingest(
            self,
            path: Path,
    ) -> IngestionResult:
        """Parse & build a reviewable draft. No DB writes."""

        return self._pipeline.ingest(path)
    

    def commit(
            self,
            result: IngestionResult,
    ) -> int:
        """Store the reviewed draft: template row + asset BLOBs + links."""

        blueprint = self._pipeline.finalize(result.draft)

        return self._repo.save(blueprint, result.assets)