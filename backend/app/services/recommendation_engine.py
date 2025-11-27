import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models.film import Film, Similarity


class RecommendationEngine:
    """Engine for computing film recommendations and similarities."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def _create_film_features(self, film: Film) -> str:
        """Create text features from film data for TF-IDF."""
        features = []
        
        # Genres (weighted more heavily)
        if film.genres:
            features.extend(film.genres * 3)  # Repeat 3 times for higher weight
        
        # Keywords
        if film.keywords:
            features.extend(film.keywords * 2)  # Repeat 2 times
        
        # Director
        if film.director:
            features.append(film.director)
        
        # Actors
        if film.actors:
            features.extend(film.actors)
        
        # Title words
        if film.titre:
            features.extend(film.titre.lower().split())
        
        return " ".join(features)
    
    def compute_similarities(
        self, 
        db: Session, 
        batch_size: int = 100
    ) -> int:
        """
        Compute similarities for all films and store in database.
        Returns number of similarity pairs created.
        """
        # Get all films
        films = db.query(Film).all()
        
        if len(films) < 2:
            return 0
        
        # Create feature strings
        film_features = [self._create_film_features(film) for film in films]
        
        # Compute TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(film_features)
        
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Clear existing similarities
        db.query(Similarity).delete()
        
        # Store top N similar films for each film
        similarities_created = 0
        top_n = 20  # Store top 20 most similar films
        
        for i, film in enumerate(films):
            # Get similarity scores for this film
            scores = similarity_matrix[i]
            
            # Get indices of top N similar films (excluding itself)
            similar_indices = np.argsort(scores)[::-1][1:top_n+1]
            
            # Create similarity records
            for similar_idx in similar_indices:
                score = float(scores[similar_idx])
                
                # Only store if similarity is significant
                if score > 0.1:
                    similarity = Similarity(
                        film_id=film.id,
                        similar_film_id=films[similar_idx].id,
                        score=score
                    )
                    db.add(similarity)
                    similarities_created += 1
        
        db.commit()
        return similarities_created
    
    def get_similar_films(
        self,
        db: Session,
        film_id: int,
        limit: int = 2
    ) -> List[Film]:
        """Get most similar films for a given film."""
        similarities = (
            db.query(Similarity)
            .filter(Similarity.film_id == film_id)
            .order_by(Similarity.score.desc())
            .limit(limit)
            .all()
        )
        
        similar_film_ids = [s.similar_film_id for s in similarities]
        
        return (
            db.query(Film)
            .filter(Film.id.in_(similar_film_ids))
            .all()
        )
    
    def get_recommendations(
        self,
        db: Session,
        selected_film_ids: List[int],
        liked_film_ids: List[int] = None,
        disliked_film_ids: List[int] = None,
        limit: int = 10
    ) -> List[Film]:
        """
        Get film recommendations based on selected films and feedback.
        
        Args:
            db: Database session
            selected_film_ids: IDs of films user selected as favorites
            liked_film_ids: IDs of recommended films user liked
            disliked_film_ids: IDs of recommended films user disliked
            limit: Number of recommendations to return
        """
        if liked_film_ids is None:
            liked_film_ids = []
        if disliked_film_ids is None:
            disliked_film_ids = []
        
        # Combine selected and liked films
        positive_film_ids = list(set(selected_film_ids + liked_film_ids))
        
        # Get all similar films with scores
        film_scores: Dict[int, float] = {}
        
        for film_id in positive_film_ids:
            similarities = (
                db.query(Similarity)
                .filter(Similarity.film_id == film_id)
                .all()
            )
            
            for sim in similarities:
                similar_id = sim.similar_film_id
                
                # Skip if already selected, liked, or disliked
                if similar_id in positive_film_ids or similar_id in disliked_film_ids:
                    continue
                
                # Accumulate scores
                if similar_id in film_scores:
                    film_scores[similar_id] += sim.score
                else:
                    film_scores[similar_id] = sim.score
        
        # Penalize disliked films' similar films
        for disliked_id in disliked_film_ids:
            similarities = (
                db.query(Similarity)
                .filter(Similarity.film_id == disliked_id)
                .all()
            )
            
            for sim in similarities:
                similar_id = sim.similar_film_id
                if similar_id in film_scores:
                    film_scores[similar_id] -= sim.score * 0.5  # Reduce score
        
        # Sort by score and get top films
        sorted_films = sorted(
            film_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        recommended_ids = [film_id for film_id, _ in sorted_films]
        
        # Fetch films maintaining order
        films = db.query(Film).filter(Film.id.in_(recommended_ids)).all()
        films_dict = {film.id: film for film in films}
        
        return [films_dict[film_id] for film_id in recommended_ids if film_id in films_dict]
