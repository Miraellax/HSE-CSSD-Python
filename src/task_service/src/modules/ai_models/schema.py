from pydantic import BaseModel

class DetectionModelBase(BaseModel):
    name: str

class DetectionModelCreate(DetectionModelBase):
    pass

class DetectionModel(DetectionModelBase):
    id: int

    class Config:
        from_attributes = True


class ClassificationModelBase(BaseModel):
    name: str

class ClassificationModelCreate(ClassificationModelBase):
    pass

class ClassificationModel(ClassificationModelBase):
    id: int

    class Config:
        from_attributes = True
