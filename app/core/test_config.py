from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class TestSettings(BaseSettings):
    """
    Settings for the testing environment.
    """
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_SERVER: str = "localhost"  # Тесты запускаем с хоста
    POSTGRES_PORT: int = 5433  # Используем порт тестовой базы
    POSTGRES_DB: str = "test_db"

    BASE_URL: str = "http://testserver"

    model_config = SettingsConfigDict(case_sensitive=True)

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


test_settings = TestSettings()
