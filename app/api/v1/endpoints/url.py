from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.url import URLCreate, URLInfo, URLStats
from app.services.url_service import URLService

router = APIRouter()


@router.post("/shorten", response_model=URLInfo, status_code=status.HTTP_201_CREATED)
async def shorten_url(url_in: URLCreate, db: AsyncSession = Depends(get_db)):
    """
    Takes a long URL and returns a shortened version.
    """
    service = URLService(db)
    # Pydantic's HttpUrl object needs to be converted to a string
    short_url = await service.create_short_url(str(url_in.original_url))
    return URLInfo(short_url=short_url)


@router.get("/{short_id}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_original(short_id: str, db: AsyncSession = Depends(get_db)):
    """
    Redirects to the original URL and increments the click counter.
    """
    service = URLService(db)
    original_url = await service.get_original_url_and_track_click(short_id)

    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=original_url)


@router.get("/stats/{short_id}", response_model=URLStats)
async def get_url_stats(short_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns click statistics for a specific short URL.
    """
    service = URLService(db)
    stats = await service.get_url_stats(short_id)

    if not stats:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return stats
