from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models

async def get_scene_class_values(db: AsyncSession) -> List[models.SceneClass]:
    q = select(models.SceneClass)

    return (await db.execute(q)).scalars().all()

async def get_scene_class_id(db: AsyncSession, scene_class: str):
    q = select(models.SceneClass).filter(models.SceneClass.scene_class == scene_class)

    return (await db.execute(q)).scalar()