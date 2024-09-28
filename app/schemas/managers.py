from pydantic import BaseModel


class SManagers(BaseModel):

    id: int
    telegram_id: int
    name: str
    fio_manager: str
    username: str


class SRegManager(BaseModel):

    telegram_id: int
    name: str
    fio_manager: str
    username: str
