from destinations.models import Destination

class RecommendationService:
    """
    Modular recommendation engine scoring destinations based on user preferences.
    """
    
    @classmethod
    def get_recommendations(cls, budget, season, travel_type, duration, num_travellers, state=None):
        """
        Scores all destinations and returns a sorted list of tuples (destination, score_percent).
        """
        destinations = Destination.objects.all()
        scored_destinations = []
        
        for dest in destinations:
            score = 0.0
            max_score = 0.0
            
            # 1. Season matching (Weight: 25)
            max_score += 25.0
            if season and season.lower() in dest.best_season.lower():
                score += 25.0
                
            # 2. Budget Level matching (Weight: 25)
            max_score += 25.0
            if budget == dest.budget_level:
                score += 25.0
            elif (budget == 'Moderate' and (dest.budget_level in ['Budget', 'Luxury'])) or \
                 (dest.budget_level == 'Moderate' and (budget in ['Budget', 'Luxury'])):
                score += 10.0
                
            # 3. Travel Type matching (Weight: 20)
            max_score += 20.0
            if travel_type == 'Solo' and dest.solo_friendly:
                score += 20.0
            elif travel_type == 'Couple' and dest.couple_friendly:
                score += 20.0
            elif travel_type == 'Family' and dest.family_friendly:
                score += 20.0
                
            # 4. Ideal Duration matching (Weight: 15)
            max_score += 15.0
            try:
                diff = abs(int(duration) - dest.ideal_days)
            except (ValueError, TypeError):
                diff = 999
                
            if diff <= 1:
                score += 15.0
            elif diff <= 3:
                score += 8.0
                
            # 5. Preferred State matching (Weight: 15, if selected)
            if state:
                max_score += 15.0
                if dest.state and dest.state.strip().lower() == state.strip().lower():
                    score += 15.0
                    
            # Calculate match percentage
            match_percentage = round((score / max_score) * 100) if max_score > 0 else 0
            scored_destinations.append((dest, match_percentage))
            
        # Sort by match percentage descending, then by average rating descending
        scored_destinations.sort(key=lambda x: (x[1], x[0].average_rating), reverse=True)
        return scored_destinations[:5]
