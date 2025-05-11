from pydantic import BaseModel

class SceneClassPredictionBase(BaseModel):
    task_id: int
    scene_class_id: int
    scene_class_prob: float

class SceneClassPredictionCreate(SceneClassPredictionBase):
    pass

class SceneClassPrediction(SceneClassPredictionBase):
    id: int

    class Config:
        from_attributes = True
