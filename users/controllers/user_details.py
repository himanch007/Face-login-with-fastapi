from fastapi import APIRouter, Header, Request

router = APIRouter()


@router.get("", status_code=200)
async def user_details(request: Request, auth_token: str = Header(alias="authorization")):
    
    user_data = request.user_data
    user_data.pop('_id')
    user_data.pop('password')

    return user_data
