from pydantic import BaseModel, HttpUrl
from datetime import datetime


# --- Request Schemas ---

class URLCreate(BaseModel):
    """
    Schema for the incoming request to shorten a URL.
    """
    original_url: HttpUrl  # Pydantic будет валидировать, что это реальный URL


# --- Response Schemas ---

class URLInfo(BaseModel):
    """
    Schema for the response after creating a short link.
    """
    short_url: str


class URLStats(BaseModel):
    """
    Schema for returning the statistics of a short link.
    """
    original_url: HttpUrl
    short_url: str
    clicks: int
    created_at: datetime
