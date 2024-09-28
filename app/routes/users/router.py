from fastapi import APIRouter

from fastapi_cache.decorator import cache

from app.views.users.view import view_get_users
from app.schemas.users import SUser

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.get(
    "/",
    description="Получение всех пользователей",
    response_model=list[SUser]
)
@cache(expire=60)
async def get_users():

    return await view_get_users()