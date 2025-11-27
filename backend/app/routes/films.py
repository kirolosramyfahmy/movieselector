from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List, Optional
from app.core.database import get_db
from app.models.film import Film
from app.models.schemas import (
    FilmResponse,
    FilmDetailResponse,
    SimilarFilmsResponse,
    RecommendationRequest,
    RecommendationResponse,
    MetadataResponse
)
from app.services.recommendation_engine import RecommendationEngine
from app.utils.cache import get_cached, set_cached

router = APIRouter(prefix="/films", tags=["films"])
recommendation_engine = RecommendationEngine()


@router.get("/popular", response_model=List[FilmResponse])
async def get_popular_films(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    sort_by: str = Query("popularity", regex="^(popularity|recent_popular)$"),
    db: Session = Depends(get_db)
):
    """Get popular films with optional filters."""
    # Create cache key
    cache_key = f"popular:{page}:{limit}:{genre}:{year}:{min_rating}:{sort_by}"
    
    # Check cache
    cached = await get_cached(cache_key)
    if cached:
        return cached
    
    # Build query
    query = db.query(Film)
    
    # Apply filters
    if genre:
        query = query.filter(Film.genres.contains([genre]))
    
    if year:
        query = query.filter(Film.annee == year)
    
    if min_rating:
        query = query.filter(Film.vote_average >= min_rating)
    
    # Filter out Indian films (User Request)
    indian_languages = ['hi', 'te', 'ta', 'ml', 'kn']
    query = query.filter(Film.original_language.notin_(indian_languages))
    
    # Filter out films without posters (User Request)
    query = query.filter(Film.poster_url.isnot(None))
    
    # Filter out unreleased films (User Request)
    # Assuming release_date is stored as string YYYY-MM-DD
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    query = query.filter(Film.release_date <= today)
    
    # Apply sorting
    if sort_by == "recent_popular":
        # Sort by year desc, then popularity desc
        query = query.order_by(Film.annee.desc(), Film.popularity.desc())
    else:
        # Default: popularity desc
        query = query.order_by(Film.popularity.desc())
    
    # Paginate
    offset = (page - 1) * limit
    films = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    result = [FilmResponse.model_validate(film) for film in films]
    
    # Cache result
    await set_cached(cache_key, [r.model_dump() for r in result])
    
    return result


@router.get("/search", response_model=List[FilmResponse])
async def search_films(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search films by title with autocomplete."""
    # Create cache key
    cache_key = f"search:{q}:{limit}"
    
    # Check cache
    cached = await get_cached(cache_key)
    if cached:
        return cached
    
    # Search in both French and original titles
    search_pattern = f"%{q}%"
    films = (
        db.query(Film)
        .filter(
            or_(
                Film.titre.ilike(search_pattern),
                Film.titre_original.ilike(search_pattern)
            )
        )
        .order_by(Film.popularity.desc())
        .limit(limit)
        .all()
    )
    
    result = [FilmResponse.model_validate(film) for film in films]
    
    # Cache result
    await set_cached(cache_key, [r.model_dump() for r in result], ttl=1800)  # 30 min
    
    return result


@router.get("/{film_id}", response_model=FilmDetailResponse)
async def get_film_details(
    film_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a film."""
    # Check cache
    cache_key = f"film:{film_id}"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    
    film = db.query(Film).filter(Film.id == film_id).first()
    
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    result = FilmDetailResponse.model_validate(film)
    
    # Cache result
    await set_cached(cache_key, result.model_dump())
    
    return result


@router.get("/{film_id}/similar", response_model=List[FilmResponse])
async def get_similar_films(
    film_id: int,
    limit: int = Query(2, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Get similar films for a given film."""
    # Check cache
    cache_key = f"similar:{film_id}:{limit}"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    
    # Check if film exists
    film = db.query(Film).filter(Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # Get similar films
    similar_films = recommendation_engine.get_similar_films(db, film_id, limit)
    
    result = [FilmResponse.model_validate(film) for film in similar_films]
    
    # Cache result
    await set_cached(cache_key, [r.model_dump() for r in result])
    
    return result


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get film recommendations based on selected films and feedback."""
    # Validate that selected films exist
    selected_films = (
        db.query(Film)
        .filter(Film.id.in_(request.selected_film_ids))
        .all()
    )
    
    if len(selected_films) != len(request.selected_film_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more selected films not found"
        )
    
    # Get recommendations
    recommended_films = recommendation_engine.get_recommendations(
        db=db,
        selected_film_ids=request.selected_film_ids,
        liked_film_ids=request.liked_film_ids or [],
        disliked_film_ids=request.disliked_film_ids or [],
        limit=request.limit
    )
    
    result = [FilmResponse.model_validate(film) for film in recommended_films]
    
    return RecommendationResponse(recommendations=result)


@router.get("/metadata/info", response_model=MetadataResponse)
async def get_metadata(db: Session = Depends(get_db)):
    """Get metadata for filters (genres, year range)."""
    # Check cache
    cache_key = "metadata:info"
    cached = await get_cached(cache_key)
    if cached:
        return cached
    
    # Get all unique genres
    all_genres = db.query(Film.genres).all()
    genres_set = set()
    for (genres,) in all_genres:
        if genres:
            genres_set.update(genres)
    
    # Get year range
    year_stats = db.query(
        func.min(Film.annee).label('min_year'),
        func.max(Film.annee).label('max_year')
    ).first()
    
    result = MetadataResponse(
        genres=sorted(list(genres_set)),
        min_year=year_stats.min_year,
        max_year=year_stats.max_year
    )
    
    # Cache for longer (metadata changes rarely)
    await set_cached(cache_key, result.model_dump(), ttl=7200)  # 2 hours
    
    return result
