from pydantic import BaseModel, Field
from typing import List, Optional


class FilmBase(BaseModel):
    """Base film schema."""
    titre: str
    titre_original: Optional[str] = None
    annee: Optional[int] = None
    genres: List[str]
    poster_url: Optional[str] = None
    popularity: float = 0.0
    vote_average: float = 0.0
    vote_count: int = 0


class FilmResponse(FilmBase):
    """Film response schema."""
    id: int
    tmdb_id: int
    overview: Optional[str] = None
    
    class Config:
        from_attributes = True


class FilmDetailResponse(FilmResponse):
    """Detailed film response with additional info."""
    overview: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class SimilarFilmsResponse(BaseModel):
    """Response for similar films."""
    film: FilmResponse
    similar_films: List[FilmResponse]


class RecommendationRequest(BaseModel):
    """Request for film recommendations."""
    selected_film_ids: List[int] = Field(..., min_items=1)
    liked_film_ids: Optional[List[int]] = None
    disliked_film_ids: Optional[List[int]] = None
    limit: int = Field(default=5, ge=1, le=20)


class RecommendationResponse(BaseModel):
    """Response with film recommendations."""
    recommendations: List[FilmResponse]


class GenreResponse(BaseModel):
    """Genre response."""
    id: int
    name: str


class MetadataResponse(BaseModel):
    """Metadata response."""
    genres: List[str]
    min_year: Optional[int] = None
    max_year: Optional[int] = None
