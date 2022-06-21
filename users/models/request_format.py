from pydantic import BaseModel, EmailStr


class LoginFormat(BaseModel):
    email: EmailStr
    password: str