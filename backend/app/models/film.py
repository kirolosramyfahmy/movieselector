from sqlalchemy import Column, Integer, String, Float, ARRAY, DateTime, Index, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Film(Base):
    """Film model."""
    __tablename__ = "films"
    
    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    titre = Column(String, nullable=False)
    titre_original = Column(String)
    original_language = Column(String)
    release_date = Column(String)  # Storing as string YYYY-MM-DD for simplicity
    annee = Column(Integer, index=True)
    genres = Column(ARRAY(String), nullable=False)
    poster_url = Column(String)
    popularity = Column(Float, default=0.0, index=True)
    vote_average = Column(Float, default=0.0, index=True)
    vote_count = Column(Integer, default=0, index=True)
    overview = Column(String)
    director = Column(String)
    actors = Column(ARRAY(String))
    keywords = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_films_popularity_vote', 'popularity', 'vote_average'),
        Index('ix_films_annee_popularity', 'annee', 'popularity'),
    )


class Similarity(Base):
    """Film similarity model."""
    __tablename__ = "similarities"
    
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey('films.id'), nullable=False, index=True)
    similar_film_id = Column(Integer, ForeignKey('films.id'), nullable=False, index=True)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Composite index for fast lookups
    __table_args__ = (
        Index('ix_similarity_film_score', 'film_id', 'score'),
    )
