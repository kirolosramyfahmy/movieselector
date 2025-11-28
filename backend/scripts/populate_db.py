"""
Script to populate database with films from TMDB and compute similarities.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.film import Film
from app.services.tmdb_service import TMDBService
from app.services.recommendation_engine import RecommendationEngine


async def fetch_and_store_films(
    db: Session,
    tmdb_service: TMDBService,
    num_pages: int = 50
):
    """Fetch films from TMDB and store in database."""
    print(f"📥 Fetching films from TMDB ({num_pages} pages)...")
    
    films_added = 0
    films_updated = 0
    
    for page in range(1, num_pages + 1):
        try:
            # Get popular films
            response = await tmdb_service.get_popular_films(page=page)
            
            for film_data in response.get("results", []):
                tmdb_id = film_data.get("id")
                
                # Check if film already exists
                existing_film = db.query(Film).filter(Film.tmdb_id == tmdb_id).first()
                
                # Fetch complete data
                try:
                    complete_data = await tmdb_service.fetch_complete_film_data(tmdb_id)
                    
                    if existing_film:
                        # Update existing film
                        for key, value in complete_data.items():
                            if key != "tmdb_id":  # Don't update tmdb_id
                                setattr(existing_film, key, value)
                        films_updated += 1
                    else:
                        # Create new film
                        film = Film(**complete_data)
                        db.add(film)
                        films_added += 1
                    
                    # Commit every 10 films
                    if (films_added + films_updated) % 10 == 0:
                        db.commit()
                        print(f"  Progress: {films_added} added, {films_updated} updated")
                
                except Exception as e:
                    print(f"  ⚠️  Error fetching film {tmdb_id}: {e}")
                    continue
            
            # Small delay to respect rate limits
            await asyncio.sleep(0.3)
            
        except Exception as e:
            print(f"  ⚠️  Error fetching page {page}: {e}")
            continue
    
    # Final commit
    db.commit()
    
    print(f"✅ Films fetched: {films_added} added, {films_updated} updated")
    return films_added, films_updated


def compute_and_store_similarities(db: Session):
    """Compute similarities between films."""
    print("🔄 Computing film similarities...")
    
    engine = RecommendationEngine()
    similarities_created = engine.compute_similarities(db)
    
    print(f"✅ Similarities computed: {similarities_created} pairs created")
    return similarities_created


async def main():
    """Main function to populate database."""
    print("🎬 Movie Recommender - Database Population")
    print("=" * 50)
    
    # Create tables
    print("📊 Creating database tables...")
    Base.metadata.drop_all(bind=engine)  # Drop existing tables to update schema
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Initialize TMDB service
        tmdb_service = TMDBService()
        
        # Fetch and store films
        films_added, films_updated = await fetch_and_store_films(
            db, 
            tmdb_service,
            num_pages=20  # Fetch 20 pages (400 films) for faster startup
        )
        
        # Compute similarities
        if films_added > 0 or films_updated > 0:
            similarities_created = compute_and_store_similarities(db)
        else:
            print("⚠️  No films to compute similarities for")
        
        print("\n" + "=" * 50)
        print("✅ Database population completed!")
        print(f"   Films: {films_added} added, {films_updated} updated")
        if films_added > 0 or films_updated > 0:
            print(f"   Similarities: {similarities_created} pairs")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
