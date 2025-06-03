from typing import Union, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..db_models import models
from . import schema as task_schema


async def get_task(db: AsyncSession, owner_id: int, task_id: int) -> Union[models.Tasks, None]:
    q = select(models.Tasks).filter(models.Tasks.owner_id == owner_id, models.Tasks.id == task_id)

    return (await db.execute(q)).scalar()

async def get_task_models(db: AsyncSession, task_id: int) -> Union[models.Tasks, None]:
    q = select(models.Tasks).filter(models.Tasks.id == task_id)
    r = (await db.execute(q)).scalar()

    return {"classification_model_id": r["classification_model_id"],
            "detection_model_id": r["detection_model_id"]}

async def get_tasks_by_owner(db: AsyncSession, owner_id: int) -> List[models.Tasks]:
    q = select(models.Tasks).filter(models.Tasks.owner_id == owner_id)

    return (await db.execute(q)).scalars().all()


async def get_task_primitives_result(db: AsyncSession, task_id: int) -> List[models.PrimitivePredictions]:
    q = select(models.PrimitivePredictions).filter(models.PrimitivePredictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()


async def get_task_scene_classes_result(db: AsyncSession, task_id: int) -> List[models.SceneClassPredictions]:
    q = select(models.SceneClassPredictions).filter(models.SceneClassPredictions.task_id == task_id)

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


async def update_task_status(db: AsyncSession, task_id: int, new_status_id: int):
    stmt = update(models.Tasks).where(models.Tasks.id == task_id).values(status_id=new_status_id)
    await db.execute(stmt)
    await db.commit()

    task = select(models.Tasks).filter(models.Tasks.id == task_id)
    return (await db.execute(task)).scalar()


async def update_task_scene_class(db: AsyncSession, task_id: int, new_scene_class_id: int):
    stmt = update(models.Tasks).where(models.Tasks.id == task_id).values(scene_class_id=new_scene_class_id)
    await db.execute(stmt)
    await db.commit()

    task = select(models.Tasks).filter(models.Tasks.id == task_id)
    return (await db.execute(task)).scalar()