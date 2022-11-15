from fastapi import APIRouter, Header, Request, Response
from middleware.http_error import Conflict, Unauthorized
from users.models.user import User
from users.utils.password import get_password_hash, verify_password
from users.utils.token import get_access_token, decode_access_token
from users.validators.user import LoginRequestFormat

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: User):
    user_data = await User.Config.objects.find_user(user)

    if user_data:
        raise Conflict()

    user.password = await get_password_hash(user.password)
    await User.Config.objects.add_user(user)
    return user


@router.post("/login", status_code=200)
async def login(request: LoginRequestFormat):
    user = await User.Config.objects.find_user(request)
    if user == False:
        raise Unauthorized(message="User does not exist")
    
    plain_password = request.password
    hashed_password = user['password']

    if await verify_password(plain_password, hashed_password):
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
    user_data = await User.Config.objects.find_user(decoded_user_token)
    return {
        "name": user_data['name'],
        "email": user_data['email'],
        "meta": user_data['meta']
    }
