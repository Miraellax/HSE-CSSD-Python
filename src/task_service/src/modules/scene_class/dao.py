from typing import List

from sqlalchemy.orm import Session

from ..db_models import models

def get_scene_class_values(db: Session) -> List[models.SceneClass]:
    return db.query(models.SceneClass).all()