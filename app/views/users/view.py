from pydantic import TypeAdapter

from app.dao.users import UsersDAO
from app.schemas.users import SUser


async def view_get_users():

    users = await UsersDAO.find_all()

    adapter = TypeAdapter(list[SUser])

    return adapter.validate_python(users)