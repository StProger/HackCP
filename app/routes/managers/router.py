from fastapi import APIRouter

from app.schemas.managers import SRegManager
from app.schemas.managers import SManagers
from app.views.managers.view import view_get_manager, view_create_manager

router = APIRouter(
    prefix="/managers",
    tags=["Менеджеры"]
)


@router.get(
    "/",
    description="Получение всех менеджеров",
    response_model=list[SManagers]
)
async def get_managers():

    return await view_get_manager()


@router.post(
    "/",
    description="Создание менеджера"
)
async def create_manager(manager_data: SRegManager):

    return await view_create_manager(manager_data)
