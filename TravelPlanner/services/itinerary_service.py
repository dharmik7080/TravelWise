import random
from attractions.models import Attraction

class ItineraryService:
    """
    Dedicated service for generating and prioritizing day-by-day travel itineraries
    entirely from local database records without external APIs.
    """
    
    @classmethod
    def generate_itinerary(cls, destination, total_days, travel_type, budget_level, regenerate=False):
        """
        Fetches all attractions, filters and ranks them based on travel type and budget,
        and distributes them evenly across the requested duration.
        """
        # Fetch all attractions belonging to the selected destination
        attractions = list(destination.attractions.all())
        
        # Shuffle initial list if regeneration requested
        if regenerate:
            random.shuffle(attractions)
            
        # Define travel type matching keywords
        type_keywords = {
            'Adventure': ['trekking', 'hiking', 'adventure sports', 'camping', 'adventure', 'trek', 'hike', 'climb'],
            'Family': ['parks', 'museums', 'gardens', 'scenic places', 'scenic', 'park', 'museum', 'garden'],
            'Couple': ['sunset points', 'lakes', 'romantic spots', 'cafes', 'sunset', 'lake', 'romantic', 'cafe'],
            'Solo': ['heritage', 'photography', 'local markets', 'walking tours', 'heritage', 'market', 'photo']
        }
        
        keywords = type_keywords.get(travel_type, [])
        
        def calculate_score(attr):
            score = 0.0
            # If category or description contains any of the target travel type keywords
            if any(kw in attr.category.lower() or kw in attr.description.lower() for kw in keywords):
                score += 100.0
            return score

        # Sort based on matching criteria and budget levels
        if budget_level == 'Budget':
            # Prefer free or low-cost attractions (entry_fee ascending)
            attractions.sort(key=lambda a: (-calculate_score(a), a.entry_fee))
        elif budget_level == 'Luxury':
            # Include premium attractions first (entry_fee descending)
            attractions.sort(key=lambda a: (-calculate_score(a), -a.entry_fee))
        else:
            # Moderate: default mixed sorting by travel type score
            attractions.sort(key=lambda a: -calculate_score(a))
            
        # Distribute attractions evenly across the travel days (Morning, Afternoon, Evening)
        slots = ['morning', 'afternoon', 'evening']
        itinerary = {}
        
        for day in range(1, total_days + 1):
            itinerary[day] = {slot: None for slot in slots}
            
        attr_idx = 0
        num_attrs = len(attractions)
        
        # Round-robin distribution to keep things even across all days
        for slot in slots:
            for day in range(1, total_days + 1):
                if attr_idx < num_attrs:
                    itinerary[day][slot] = attractions[attr_idx].attraction_name
                    attr_idx += 1
                    
        # Apply standard fallback options if slots remain unfilled
        for day in range(1, total_days + 1):
            if not itinerary[day]['morning']:
                itinerary[day]['morning'] = f"Explore scenic spots in {destination.destination_name}"
            if not itinerary[day]['afternoon']:
                itinerary[day]['afternoon'] = f"Visit local markets and enjoy regional cuisine"
            if not itinerary[day]['evening']:
                itinerary[day]['evening'] = f"Relax and enjoy evening views in {destination.destination_name}"
                
        return itinerary
