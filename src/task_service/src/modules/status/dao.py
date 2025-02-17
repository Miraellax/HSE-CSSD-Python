from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models


async def get_status_values(db: AsyncSession) -> List[models.Status]:
    q = select(models.Status)

    return (await db.execute(q)).scalars().all()