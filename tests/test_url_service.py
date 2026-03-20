import pytest
from unittest.mock import AsyncMock
from app.services.url_service import URLService
from app.models.url import URL
from app.core.config import settings

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_short_url_new_entry():
    """
    Unit Test: Verify that a new short URL is generated and saved 
    when the original URL does not exist in the database.
    """
    # 1. Arrange: Мокаем подключение к БД и сам репозиторий
    mock_db = AsyncMock()
    service = URLService(db=mock_db)
    service.url_repo = AsyncMock()

    # Настраиваем поведение моков: оригинального URL нет, коллизий short_id тоже нет
    service.url_repo.get_by_original_url.return_value = None
    service.url_repo.get_by_short_id.return_value = None

    original_url = "https://new-website.com"

    # 2. Act: Вызываем тестируемый метод
    result = await service.create_short_url(original_url)

    # 3. Assert: Проверяем, что метод create был вызван ровно один раз
    assert result.startswith(settings.BASE_URL)
    service.url_repo.create.assert_called_once()

    # Проверяем, что в базу передался правильный оригинальный URL
    _, kwargs = service.url_repo.create.call_args
    assert kwargs["original_url"] == original_url


async def test_create_short_url_existing_entry():
    """
    Unit Test: Verify that if the original URL already exists, 
    the service returns the existing short URL without creating a new one.
    """
    # 1. Arrange
    mock_db = AsyncMock()
    service = URLService(db=mock_db)
    service.url_repo = AsyncMock()

    # Настраиваем мок: БД отвечает, что такой URL уже сокращали
    existing_url = URL(original_url="https://existing.com", short_id="EX1234")
    service.url_repo.get_by_original_url.return_value = existing_url

    # 2. Act
    result = await service.create_short_url("https://existing.com")

    # 3. Assert: Проверяем, что вернулась старая ссылка, а новая не создавалась
    assert result == f"{settings.BASE_URL}/EX1234"
    service.url_repo.create.assert_not_called()


async def test_get_original_url_and_track_click():
    """
    Unit Test: Verify that fetching a short URL increments the click counter 
    and returns the original URL.
    """
    # 1. Arrange
    mock_db = AsyncMock()
    service = URLService(db=mock_db)
    service.url_repo = AsyncMock()

    # Настраиваем мок: ссылка найдена в базе
    mock_url = URL(original_url="https://target.com", short_id="TRG123")
    service.url_repo.get_by_short_id.return_value = mock_url

    # 2. Act
    result = await service.get_original_url_and_track_click("TRG123")

    # 3. Assert: Проверяем возврат и вызов счетчика
    assert result == "https://target.com"
    service.url_repo.increment_clicks.assert_called_once_with("TRG123")
