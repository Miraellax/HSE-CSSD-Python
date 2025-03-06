import datetime

from pydantic import BaseModel

class TaskBase(BaseModel):
    owner_id: int
    detection_model_id: int
    classification_model_id: int
    status_id: int
    input_path: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime.datetime
    scene_class_id: int | None

    class Config:
        from_attributes = True
