from pydantic import BaseModel, EmailStr, validator


class LoginFormat(BaseModel):
    email: EmailStr
    password: str