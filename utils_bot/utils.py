import requests

from app.dao.users import UsersDAO
from app.models.users import Users
from app.config import settings


async def check_user(
        user_id: int,
        business_id: str | None,
        username: str | None,
        first_name: str | None,
        last_name: str | None
):

    user: Users | None = await UsersDAO.find_by_id(user_id)

    if user is None:

        new_user = await UsersDAO.add(
            id=user_id,
            business_id=business_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        return new_user

    return user


async def update_token():
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {"yandexPassportOauthToken": settings.OAUTH_TOKEN_YAND}

        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, json=data)
        print(f"Статус: {response.status_code}", flush=True)

        response_data = response.json()
        print(f"Данные: {response_data}", flush=True)
        token = response_data['iamToken']
        print(f"Новый токен: {token}", flush=True)
        settings.IAM_TOKEN = token
    except Exception as e:
        print(f"Не получилось обновить токен: {e}", flush=True)
