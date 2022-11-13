from middleware.http_error import Unauthorized
from fastapi.requests import Request
from users.controllers.user import router as user_router
from config.settings import EXCEPTION_ROUTES
from users.utils.token import decode_access_token

async def authentication_dependency(request: Request):
    '''
    Function to check for authentication
    '''
    auth_token = request.headers.get('authorization')

    path = request.scope['path']

    if path not in EXCEPTION_ROUTES:
        if auth_token is None:
            raise Unauthorized()
        else:
            try:
                payload = await decode_access_token(auth_token.split()[1])
                print("Code for single login will be here")
            except:
                raise Unauthorized()
