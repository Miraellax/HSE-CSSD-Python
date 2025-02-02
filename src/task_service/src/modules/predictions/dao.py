from typing import List

from sqlalchemy.orm import Session

from ..db_models import models


def get_predictions(db: Session, task_id: int) -> List[models.Predictions]:
    return (db.query(models.Predictions)
            .filter(models.Predictions.task_id == task_id)
            .all()
            )