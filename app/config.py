from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_HOST: SecretStr = "localhost"
    MONGO_PORT: SecretStr = "27017"
    MONGO_USER: SecretStr = "solega"
    MONGO_PASSWORD: SecretStr = "solega"
    MONGO_DB: SecretStr = "scraper"

    class config:
        env_file = ".env.dev"


settings = Settings()
