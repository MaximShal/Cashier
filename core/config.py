from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Cashier"
    DATABASE_URL: str
    DEBUG: bool = False
    SECRET_KEY: str = "secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
