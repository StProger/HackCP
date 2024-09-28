from pydantic_settings import BaseSettings, SettingsConfigDict

from yarl import URL

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    PATH_LOGS: str = "data/logs.log"

    OAUTH_TOKEN_YAND: str
    IAM_TOKEN: str = "t1.9euelZrJyZOTlJHInJaQycbGkZScje3rnpWanMaek5HJyI6cnY3NycfKl5fl8_cQUjhI-e9ob10f_t3z91AANkj572hvXR_-zef1656VmpjGx5KOnZyTzYuSks3Kncyd7_zF656VmpjGx5KOnZyTzYuSks3Kncyd.173j8vyBY4iNcfNUDUqMYuOU2MDANZMzGQSY-BvgTxxs7QC9Y9aaD7VwTONRwihxbuSRl30aMY-uxzKHXs-tAQ"

    @property
    def db_url(self):

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def redis_url(self):
        return str(URL.build(
            scheme="redis",
            host=self.REDIS_HOST
        ))


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

APP_SCHEDULER = AsyncIOScheduler(timezone="Europe/Moscow")
