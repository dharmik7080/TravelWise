from services.ml_recommendation import MLRecommendationService

class RecommendationService:
    """
    Modular recommendation engine scoring destinations based on user preferences.
    Delegates to the hybrid machine learning and preference recommendation service.
    """
    
    @classmethod
    def get_recommendations(cls, budget, season, travel_type, duration, num_travellers, state=None):
        """
        Scores all destinations and returns a sorted list of tuples (destination, score_percent).
        """
        return MLRecommendationService.get_hybrid_recommendations(
            budget=budget,
            season=season,
            travel_type=travel_type,
            duration=duration,
            num_travellers=num_travellers,
            state=state
        )
