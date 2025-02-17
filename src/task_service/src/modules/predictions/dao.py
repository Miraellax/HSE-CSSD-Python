from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models


async def get_predictions(db: AsyncSession, task_id: int) -> List[models.Predictions]:
    q = select(models.Predictions).filter(models.Predictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()