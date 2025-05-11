from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_models import models
from . import schema as predictions_schema


async def get_predictions(db: AsyncSession, task_id: int) -> List[predictions_schema.Prediction]:
    q = select(models.Predictions).filter(models.Predictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()

async def post_predictions(db: AsyncSession, predictions: list[predictions_schema.PredictionCreate]):
    for pred in predictions:
        pred_model = models.Predictions(task_id=pred.task_id,
                            primitive_class_id=pred.primitive_class_id,
                            x_coord=pred.x_coord,
                            y_coord=pred.y_coord,
                            width=pred.width,
                            height=pred.height,
                            rotation=pred.rotation,
                            probability=pred.probability)
        db.add(pred_model)

    await db.commit()
