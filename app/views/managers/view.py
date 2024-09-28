from pydantic import TypeAdapter

from app.schemas.managers import SManagers, SRegManager
from app.dao.managers import ManagersDAO


async def view_get_manager():

    managers = await ManagersDAO.find_all()

    adapter = TypeAdapter(list[SManagers])

    return adapter.validate_python(managers)


async def view_create_manager(data: SRegManager):

    is_manager = await ManagersDAO.find_one_or_none(username=data.username)

    if is_manager:

        raise ...

    new_manager = await ManagersDAO.add(
        telegram_id=data.telegram_id,
        name=data.name,
        fio_manager=data.fio_manager,
        username=data.username
    )

    return {
        "id": new_manager.id,
    }


