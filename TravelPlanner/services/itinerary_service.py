from services.ml.itinerary_optimizer import ItineraryOptimizer

class ItineraryService:
    """
    Dedicated service for generating and prioritizing day-by-day travel itineraries.
    Delegates to the intelligent heuristics optimizer engine.
    """
    
    @classmethod
    def generate_itinerary(cls, destination, total_days, travel_type, budget_level, regenerate=False):
        """
        Generates daily itinerary mapping day-by-day slots to optimized scheduled attractions.
        """
        return ItineraryOptimizer.optimize(
            destination=destination,
            total_days=total_days,
            travel_type=travel_type,
            budget_level=budget_level,
            regenerate=regenerate
        )
