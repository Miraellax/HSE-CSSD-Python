from typing import Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models
from . import schema as task_schema


# GET api/tasks/{id:integer}        +
# GET api/tasks                     +
# GET api/tasks/{id}/input          +
# GET tasks/{id}/result             +
# POST api/tasks                    +
# DELETE api/tasks/{id:integer}


async def get_task(db: AsyncSession, owner_id: int, task_id: int) -> Union[models.Tasks, None]:
    q = select(models.Tasks).filter(models.Tasks.owner_id == owner_id, models.Tasks.id == task_id)

    return (await db.execute(q)).scalar()


async def get_tasks_by_owner(db: AsyncSession, owner_id: int) -> List[models.Tasks]:
    q = select(models.Tasks).filter(models.Tasks.owner_id == owner_id)

    return (await db.execute(q)).scalars().all()


async def get_task_result(db: AsyncSession, task_id: int) -> List[models.Predictions]:
    q = select(models.Predictions).filter(models.Predictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()


async def create_task(db: AsyncSession, task: task_schema.TaskCreate):
    task = models.Tasks(owner_id=task.owner_id,
                        detection_model_id=task.detection_model_id,
                        classification_model_id=task.classification_model_id,
                        status_id=task.status_id,
                        input_path=task.input_path)

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def delete_task(db: AsyncSession, task: models.Tasks) -> Union[int, None]:
    await db.delete(task)
    await db.commit()

    return task.id