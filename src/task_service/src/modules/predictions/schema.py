from pydantic import BaseModel

class PredictionBase(BaseModel):
    task_id: int
    primitive_class_id: int
    x_coord: float
    y_coord: float
    width: float
    height: float
    rotation: float
    probability: float

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int

    class Config:
        from_attributes = True
