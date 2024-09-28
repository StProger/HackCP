from pydantic import TypeAdapter

from app.dao.dialogs import DialogsDAO
from app.schemas.dialogs import SDialogs


async def view_get_all_dialogs():

    dialogs = await DialogsDAO.find_all()

    adapter = TypeAdapter(list[SDialogs])

    return adapter.validate_python(dialogs)


async def view_get_dialog(user_id):

    dialog = await DialogsDAO.find_all(user_id=user_id)

    adapter = TypeAdapter(list[SDialogs])

    return adapter.validate_python(dialog)
