from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.url import URL


class URLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_short_id(self, short_id: str) -> Optional[URL]:
        query = select(URL).where(URL.short_id == short_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_original_url(self, original_url: str) -> Optional[URL]:
        query = select(URL).where(URL.original_url == original_url)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, original_url: str, short_id: str) -> URL:
        new_url = URL(original_url=original_url, short_id=short_id)
        self.session.add(new_url)
        await self.session.commit()
        await self.session.refresh(new_url)
        return new_url

    async def increment_clicks(self, short_id: str) -> None:
        """
        Atomically increments the click counter for a URL in the database.
        This prevents race conditions.
        """
        query = (
            update(URL)
            .where(URL.short_id == short_id)
            .values(clicks=URL.clicks + 1)
        )
        await self.session.execute(query)
        await self.session.commit()
