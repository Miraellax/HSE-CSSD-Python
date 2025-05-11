from pydantic import BaseModel

class PrimitivePredictionBase(BaseModel):
    task_id: int
    primitive_class_id: int
    x1_coord: float
    y1_coord: float
    x2_coord: float
    y2_coord: float
    x3_coord: float
    y3_coord: float
    x4_coord: float
    y4_coord: float
    probability: float

class PrimitivePredictionCreate(PrimitivePredictionBase):
    pass

class PrimitivePrediction(PrimitivePredictionBase):
    id: int

    class Config:
        from_attributes = True
