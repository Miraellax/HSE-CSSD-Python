from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db_models import models
from . import schema as predictions_schema


async def get_predictions(db: AsyncSession, task_id: int) -> List[predictions_schema.PrimitivePrediction]:
    q = select(models.PrimitivePredictions).filter(models.PrimitivePredictions.task_id == task_id)

    return (await db.execute(q)).scalars().all()

async def post_primitive_predictions(db: AsyncSession, predictions: list[predictions_schema.PrimitivePredictionCreate]):
    for pred in predictions:
        pred_model = models.PrimitivePredictions(task_id=pred.task_id,
                            primitive_class_id=pred.primitive_class_id,
                            x1_coord=pred.x1_coord,
                            y1_coord=pred.y1_coord,
                            x2_coord=pred.x2_coord,
                            y2_coord=pred.y2_coord,
                            x3_coord=pred.x3_coord,
                            y3_coord=pred.y3_coord,
                            x4_coord=pred.x4_coord,
                            y4_coord=pred.y4_coord,
                            probability=pred.probability)
        db.add(pred_model)

    await db.commit()
