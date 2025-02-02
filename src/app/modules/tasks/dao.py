from typing import Union, List

from sqlalchemy.orm import Session

from ..db_models import models
from . import schema as task_schema


# GET api/tasks/{id:integer}        +
# GET api/tasks                     +
# GET api/tasks/{id}/input          +
# GET tasks/{id}/result             +
# POST api/tasks                    +
# DELETE api/tasks/{id:integer}


def get_task(db: Session, owner_id: int, task_id: int) -> Union[models.Tasks, None]:
    return (db.query(models.Tasks)
            .filter(models.Tasks.owner_id == owner_id, models.Tasks.id == task_id)
            .first()
            )


def get_tasks_by_owner(db: Session, owner_id: int) -> List[models.Tasks]:
    # return db.query(models.Tasks).filter(models.Tasks.owner_id == owner_id).all()
    return (db.query(models.Tasks)
            .filter(models.Tasks.owner_id == owner_id)
            .all()
            )


def get_task_result(db: Session, task_id: int) -> List[models.Predictions]:
    return (db.query(models.Predictions)
            .filter(models.Predictions.task_id == task_id)
            .all()
            )


def create_task(db: Session, task: task_schema.TaskCreate):
    task = models.Tasks(owner_id=task.owner_id,
                        detection_model_id=task.detection_model_id,
                        classification_model_id=task.classification_model_id,
                        status_id=task.status_id,
                        input_path=task.input_path)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task: models.Tasks) -> Union[int, None]:
    db.delete(task)
    db.commit()

    return task.id