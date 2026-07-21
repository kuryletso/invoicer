from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.assets.repository import save_assets
from app.assets.service import AssetBlob
from app.db.associations import template_asset_m2m
from app.db.models.core.assets import Asset
from app.db.models.core.template import Template
from app.document_engine.blueprint.models.template import TemplateBlueprint
from app.document_engine.blueprint.assets import collect_assets_ids
from app.document_engine.blueprint.serialize import dump_blueprint, load_blueprint
from app.services.errors import EntityNotFound


class TemplateRepository:

    def __init__(
            self,
            session: Session,
    ) -> None:
        
        self._session = session


    def save(
            self,
            blueprint: TemplateBlueprint,
            bundle: Mapping[str, AssetBlob],
    ) -> int:
        
        referenced = collect_assets_ids(blueprint)
        sections, placeholders, config = dump_blueprint(blueprint)

        template = Template(
            name=blueprint.config.name,
            type=blueprint.config.type,
            sections=sections,
            placeholders=placeholders,
            config=config,
        )
        self._session.add(template)
        self._session.flush()

        save_assets(
            self._session,
            { h: bundle[h] for h in referenced if h in bundle },
        )

        for sha in referenced:
            self._session.execute(
                template_asset_m2m.insert().values(
                    template_id=template.id,
                    asset_sha256=sha,
                )
            )

        self._session.commit()
        return template.id
    

    def get(
            self,
            template_id: int,
    ) -> TemplateBlueprint:
        
        row = self._session.get(Template, template_id)
        if row is None:
            raise EntityNotFound(
                f"template {template_id} not found",
                context={"template_id": template_id},
            )
        
        return load_blueprint(
            row.sections,
            row.placeholders,
            row.config,
        )
    

    def delete(
            self,
            template_id: int,
    ) -> None:
        
        row = self._session.get(Template, template_id)
        if row is None:
            raise EntityNotFound(
                f"template {template_id} not found",
                context={"template_id": template_id},
            )
        
        # drop the template's references, then the template
        self._session.execute(
            delete(template_asset_m2m).where(template_asset_m2m.c.template_id == template_id)
        )
        self._session.delete(row)

        # garbage collection of any asset with no remaining reference (verified set-difference)
        referenced = select(template_asset_m2m.c.asset_sha256)
        self._session.execute(delete(Asset).where(Asset.sha256.not_in(referenced)))

        self._session.commit()