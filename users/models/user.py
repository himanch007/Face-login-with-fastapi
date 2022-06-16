from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def name_is_required(cls, v):
        if v == '':
            raise ValueError('name is required')
        return v

    @validator('password')
    def password_is_required(cls, v):
        if v == '':
            raise ValueError('password is required')
        return v

    class Config:
        fields = {'password': {'exclude': True}}