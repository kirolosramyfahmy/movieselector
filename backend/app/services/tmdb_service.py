import httpx
from typing import List, Dict, Any, Optional
from app.core.config import get_settings

settings = get_settings()


class TMDBService:
    """Service for interacting with TMDB API."""
    
    def __init__(self):
        self.api_key = settings.tmdb_api_key
        self.base_url = settings.tmdb_base_url
        self.image_base_url = "https://image.tmdb.org/t/p/w780"
        
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make request to TMDB API."""
        if params is None:
            params = {}
        
        params["api_key"] = self.api_key
        params["language"] = "fr-FR"  # French language
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_popular_films(
        self, 
        page: int = 1,
        region: str = "FR"
    ) -> Dict[str, Any]:
        """Get popular films."""
        params = {"page": page, "region": region}
        return await self._make_request("/movie/popular", params)
    
    async def search_films(
        self, 
        query: str, 
        page: int = 1
    ) -> Dict[str, Any]:
        """Search films by query."""
        params = {"query": query, "page": page}
        return await self._make_request("/movie/search", params)
    
    async def get_film_details(self, tmdb_id: int) -> Dict[str, Any]:
        """Get detailed information about a film."""
        return await self._make_request(f"/movie/{tmdb_id}")
    
    async def get_film_credits(self, tmdb_id: int) -> Dict[str, Any]:
        """Get film credits (cast and crew)."""
        return await self._make_request(f"/movie/{tmdb_id}/credits")
    
    async def get_film_keywords(self, tmdb_id: int) -> Dict[str, Any]:
        """Get film keywords."""
        return await self._make_request(f"/movie/{tmdb_id}/keywords")
    
    async def get_similar_films(self, tmdb_id: int, page: int = 1) -> Dict[str, Any]:
        """Get similar films from TMDB."""
        params = {"page": page}
        return await self._make_request(f"/movie/{tmdb_id}/similar", params)
    
    async def discover_films(
        self,
        page: int = 1,
        sort_by: str = "popularity.desc",
        with_genres: Optional[str] = None,
        year: Optional[int] = None,
        vote_average_gte: Optional[float] = None
    ) -> Dict[str, Any]:
        """Discover films with filters."""
        params = {
            "page": page,
            "sort_by": sort_by
        }
        
        if with_genres:
            params["with_genres"] = with_genres
        if year:
            params["year"] = year
        if vote_average_gte:
            params["vote_average.gte"] = vote_average_gte
            
        return await self._make_request("/discover/movie", params)
    
    async def get_genre_list(self) -> Dict[str, Any]:
        """Get list of official genres."""
        return await self._make_request("/genre/movie/list")
    
    def get_poster_url(self, poster_path: Optional[str]) -> Optional[str]:
        """Get full poster URL."""
        if not poster_path:
            return None
        return f"{self.image_base_url}{poster_path}"
    
    async def fetch_complete_film_data(self, tmdb_id: int) -> Dict[str, Any]:
        """Fetch complete film data including details, credits, and keywords."""
        details = await self.get_film_details(tmdb_id)
        credits = await self.get_film_credits(tmdb_id)
        keywords = await self.get_film_keywords(tmdb_id)
        
        # Extract director
        director = None
        for crew_member in credits.get("crew", []):
            if crew_member.get("job") == "Director":
                director = crew_member.get("name")
                break
        
        # Extract top actors (first 5)
        actors = [
            cast_member.get("name") 
            for cast_member in credits.get("cast", [])[:5]
        ]
        
        # Extract keywords
        keyword_list = [
            kw.get("name") 
            for kw in keywords.get("keywords", [])
        ]
        
        return {
            "tmdb_id": details.get("id"),
            "titre": details.get("title"),
            "titre_original": details.get("original_title"),
            "original_language": details.get("original_language"),
            "release_date": details.get("release_date"),
            "annee": int(details.get("release_date", "")[:4]) if details.get("release_date") else None,
            "genres": [genre.get("name") for genre in details.get("genres", [])],
            "poster_url": self.get_poster_url(details.get("poster_path")),
            "popularity": details.get("popularity", 0.0),
            "vote_average": details.get("vote_average", 0.0),
            "overview": details.get("overview"),
            "director": director,
            "actors": actors,
            "keywords": keyword_list
        }
