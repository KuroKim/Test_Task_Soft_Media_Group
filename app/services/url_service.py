import secrets
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.url_repo import URLRepository
from app.core.config import settings


class URLService:
    def __init__(self, db: AsyncSession):
        self.url_repo = URLRepository(db)

    async def create_short_url(self, original_url: str) -> str:
        """
        Creates a short URL. If the original URL already exists, returns the existing short URL.
        """
        # 1. Check if URL is already shortened
        existing = await self.url_repo.get_by_original_url(original_url)
        if existing:
            return f"{settings.BASE_URL}/{existing.short_id}"

        # 2. Generate a unique short_id
        while True:
            short_id = secrets.token_urlsafe(6)
            if not await self.url_repo.get_by_short_id(short_id):
                break

        # 3. Create new entry
        await self.url_repo.create(original_url=original_url, short_id=short_id)
        return f"{settings.BASE_URL}/{short_id}"

    async def get_original_url_and_track_click(self, short_id: str) -> Optional[str]:
        """
        Retrieves the original URL and atomically increments the click counter.
        """
        url_record = await self.url_repo.get_by_short_id(short_id)
        if url_record:
            await self.url_repo.increment_clicks(short_id)
            return url_record.original_url
        return None

    async def get_url_stats(self, short_id: str) -> Optional[dict]:
        """
        Retrieves statistics for a short URL.
        """
        url_record = await self.url_repo.get_by_short_id(short_id)
        if url_record:
            return {
                "original_url": url_record.original_url,
                "short_url": f"{settings.BASE_URL}/{url_record.short_id}",
                "clicks": url_record.clicks,
                "created_at": url_record.created_at,
            }
        return None
