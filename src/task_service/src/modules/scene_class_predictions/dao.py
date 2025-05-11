from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_models import models
from . import schema as scene_class_predictions_schema


async def get_scene_class_predictions(db: AsyncSession, task_id: int) -> List[scene_class_predictions_schema.SceneClassPrediction]:
    q = select(models.SceneClassPredictions).filter(models.SceneClassPredictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()

async def post_scene_class_predictions(db: AsyncSession, predictions: list[scene_class_predictions_schema.SceneClassPredictionCreate]):
    for pred in predictions:
        pred_model = models.SceneClassPredictions(task_id=pred.task_id,
                                                  scene_class_id=pred.scene_class_id,
                                                  scene_class_prob=pred.scene_class_prob)
        db.add(pred_model)

    await db.commit()
