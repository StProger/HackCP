from fastapi import APIRouter

from pydantic import TypeAdapter

from fastapi_cache.decorator import cache

from app.views.dialogs.view import view_get_all_dialogs, view_get_dialog

from app.schemas.dialogs import SDialogs

router = APIRouter(
    prefix="/dialogs",
    tags=["История диалога"]
)


@router.get(
    "/{user_id}",
    description="Получение истории диалога по id юзера",
    response_model=list[SDialogs]
)
@cache(expire=60)
async def get_dialog(user_id: int):

    return await view_get_dialog(user_id)

@router.get(
    "/",
    description="Получение всех диалогов",
    response_model=list[SDialogs]
)
@cache(expire=60)
async def get_all_dialogs():

    return await view_get_all_dialogs()



