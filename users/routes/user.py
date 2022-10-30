from fastapi import APIRouter, Header, Request, Response
from middleware.http_error import Conflict, Unauthorized
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
        raise Conflict()

    user.password = get_password_hash(user.password)
    await add_user(user)
    return user


@router.post("/login", status_code=200)
async def login(request: LoginFormat, response: Response):
    user = await find_user(request)
    if user == False:
        raise Unauthorized(message="User does not exist")
    
    plain_password = request.password
    hashed_password = user['password']

    if verify_password(plain_password, hashed_password):
        access_token = await get_access_token(user)
        # code to store token in db for single login
    else:
        raise Unauthorized(message="Incorrect password")
    return {
        "access_token": access_token
    }


@router.get("/user-details", status_code=200)
async def user_details(request: Request, auth_token: str = Header(alias="authorization")):
    access_token = request.headers.get('authorization')
    decoded_user_token = await decode_access_token(access_token.split()[1])
    user_data = await find_user(decoded_user_token)
    return {
        "name": user_data['name'],
        "email": user_data['email'],
        "meta": user_data['meta']
    }