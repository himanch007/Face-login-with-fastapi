from fastapi import APIRouter
from middleware.http_error import Conflict
from users.models.user import User
from users.utils.password import get_password_hash

router = APIRouter()


@router.post("", status_code=201)
async def register(request_body: User):
    request_data = request_body.dict()
    user_data = await User.Config.objects.find_user(email=request_data['email'])

    if user_data:
        raise Conflict()

    request_data['password'] = await get_password_hash(request_data['password'])
    await User.Config.objects.add_user(request_data)

    return {'message': 'user has been created'}
