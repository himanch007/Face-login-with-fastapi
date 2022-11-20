from fastapi import APIRouter, Header, Request, Response
from middleware.http_error import Conflict, Unauthorized
from users.models.user import User
from users.utils.password import get_password_hash, verify_password
from users.utils.token import get_access_token, decode_access_token
from users.validators.user import LoginRequestFormat

router = APIRouter()


@router.post("/register", status_code=201)
async def register(request_body: User):
    request_body = request_body.dict()
    user_data = await User.Config.objects.find_user(email=request_body['email'])
    
    if user_data:
        raise Conflict()

    request_body['password'] = await get_password_hash(request_body['password'])
    await User.Config.objects.add_user(request_body)
    request_body.pop('password')
    return request_body


@router.post("/login", status_code=200)
async def login(request_body: LoginRequestFormat):
    request_body = request_body.dict()
    user = await User.Config.objects.find_user(email=request_body['email'])
    if user == False:
        raise Unauthorized(message="User does not exist")
    
    plain_password = request_body['password']
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
    decoded_user_token = await decode_access_token(auth_token.split()[1])
    user_data = await User.Config.objects.find_user(user_id=decoded_user_token['id'])
    user_data.pop('_id')
    user_data.pop('password')
    return user_data
