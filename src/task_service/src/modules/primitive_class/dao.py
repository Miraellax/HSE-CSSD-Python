from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models

async def get_primitive_class_values(db: AsyncSession) -> List[models.PrimitiveClass]:
    q = select(models.PrimitiveClass)

    return (await db.execute(q)).scalars().all()


async def get_primitive_class_id(db: AsyncSession, primitive_class: str):
    q = select(models.PrimitiveClass).filter(models.PrimitiveClass.primitive_class == primitive_class)

    return (await db.execute(q)).scalar()
