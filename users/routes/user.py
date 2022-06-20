from fastapi import APIRouter, Request, Response, status
from users.models.user import User
from users.utils.password import get_password_hash, verify_password
from users.utils.user import find_user, add_user
from users.utils.token import get_access_token, decode_access_token
from users.models.request_format import LoginFormat

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: User, response: Response):
    user_data = await find_user(user)
    if user_data:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "message": "user already exists"
        }
        
    user.password = get_password_hash(user.password)
    await add_user(user)
    return user


@router.post("/login")
async def login(request: LoginFormat, response: Response):
    user = await find_user(request)
    if user:
        plain_password = request.password
        hashed_password = user['password']
        if verify_password(plain_password, hashed_password):
            access_token = await get_access_token(user)
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "message": "incorrect password"
            }
        return {
            "access_token": access_token
        }
    else:
        return {
            "message": "user doesn't exist"
        }


@router.get("/user_details")
async def user_details(request: Request):
    access_token = request.headers.get('authorization')
    decoded_user_token = await decode_access_token(access_token.split()[1])
    user_data = await find_user(decoded_user_token)
    return {
        "name": user_data['name'],
        "email": user_data['email'],
        "meta": user_data['meta']
    }