from typing import List

from sqlalchemy.orm import Session

from ..db_models import models

def get_primitive_class_values(db: Session) -> List[models.PrimitiveClass]:
    return db.query(models.PrimitiveClass).all()