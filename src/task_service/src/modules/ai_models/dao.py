from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models


async def get_classification_models(db: AsyncSession) -> List[models.ClassificationModels]:
    q = select(models.ClassificationModels)

    return (await db.execute(q)).scalars().all()

async def get_detection_models(db: AsyncSession) -> List[models.DetectionModels]:
    q = select(models.DetectionModels)

    return (await db.execute(q)).scalars().all()
