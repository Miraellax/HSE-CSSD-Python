from pydantic import BaseModel

class PrimitiveClassBase(BaseModel):
    primitive_class: str

class PrimitiveClassCreate(PrimitiveClassBase):
    pass

class PrimitiveClass(PrimitiveClassBase):
    id: int

    class Config:
        from_attributes = True