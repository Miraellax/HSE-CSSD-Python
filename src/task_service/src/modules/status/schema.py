from pydantic import BaseModel

class StatusBase(BaseModel):
    status: str

class StatusCreate(StatusBase):
    pass

class Status(StatusBase):
    id: int

    class Config:
        from_attributes = True