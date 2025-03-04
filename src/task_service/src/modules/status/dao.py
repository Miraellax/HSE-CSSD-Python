from typing import List

from sqlalchemy.orm import Session

from ..db_models import models


def get_status_values(db: Session) -> List[models.Status]:
    return db.query(models.Status).all()