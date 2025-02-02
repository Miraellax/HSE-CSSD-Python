from pydantic import BaseModel

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    username: str
    hashed_password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
