from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://movie_user:movie_password@localhost:5432/movie_recommender"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # TMDB API
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    
    # Backend
    backend_port: int = 8000
    backend_host: str = "0.0.0.0"
    debug: bool = True
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Cache
    cache_ttl_seconds: int = 3600
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
