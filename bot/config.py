from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: SecretStr
    ADMIN_TG_ID: SecretStr
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')


config = Settings()
ADMIN_TG_ID = config.ADMIN_TG_ID.get_secret_value()
TOKEN = config.TOKEN.get_secret_value()


LANGUAGE_LIST = ['python', 'go', 'rust']
