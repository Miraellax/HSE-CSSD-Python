from pydantic import BaseModel

class SceneClassBase(BaseModel):
    scene_class: str

class SceneClassCreate(SceneClassBase):
    pass

class SceneClass(SceneClassBase):
    id: int

    class Config:
        from_attributes = True