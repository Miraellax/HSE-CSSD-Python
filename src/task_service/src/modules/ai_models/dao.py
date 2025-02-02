from typing import List

from sqlalchemy.orm import Session

from ..db_models import models


def get_classification_models(db: Session) -> List[models.ClassificationModels]:
    return db.query(models.ClassificationModels).all()

def get_detection_models(db: Session) -> List[models.DetectionModels]:
    return db.query(models.DetectionModels).all()