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
            
        # Overview (Synopsis) - Adds semantic context
        if film.overview:
            # Give overview words less weight than keywords/genres but valuable context
            features.extend(film.overview.lower().split())
        
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
        Includes quality re-ranking to favor better-rated films.
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
        
        # Initial sort by raw similarity
        sorted_candidates = sorted(
            film_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Take a larger pool of candidates for re-ranking (e.g. 3x the limit)
        # This allows us to filter out low-quality films that might be highly similar
        pool_size = limit * 3
        top_candidate_ids = [film_id for film_id, _ in sorted_candidates[:pool_size]]
        
        if not top_candidate_ids:
            return []
            
        # Fetch candidate films to get their ratings
        candidates = db.query(Film).filter(Film.id.in_(top_candidate_ids)).all()
        candidate_map = {f.id: f for f in candidates}
        
        # Re-rank based on Quality Score
        # Final Score = Similarity * (1 + Rating Boost)
        # This gives a slight edge to better movies without ignoring similarity
        final_scores = []
        
        for film_id, raw_score in sorted_candidates[:pool_size]:
            film = candidate_map.get(film_id)
            if not film:
                continue
                
            # Normalize rating (0-10) to a boost factor (0.0 - 0.5)
            # A 10/10 movie gets a 50% score boost. A 0/10 movie gets 0% boost.
            rating_boost = (film.vote_average or 0) / 20.0 
            
            final_score = raw_score * (1 + rating_boost)
            final_scores.append((film, final_score))
            
        # Sort by final quality-adjusted score
        final_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N films
        return [item[0] for item in final_scores[:limit]]
