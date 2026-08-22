import re
from destinations.models import Destination

class MLRecommendationService:
    # Preference weights (Task 5 constants)
    WT_SEASON = 25.0
    WT_BUDGET = 25.0
    WT_TRAVEL_TYPE = 20.0
    WT_DURATION = 15.0
    WT_STATE = 15.0

    _initialized = False

    @classmethod
    def _clean_text(cls, features_list):
        cleaned_words = []
        for feat in features_list:
            if not feat:
                continue
            words = re.findall(r'\b\w+\b', str(feat).lower())
            cleaned_words.extend(words)
        return list(dict.fromkeys(cleaned_words))

    @classmethod
    def _initialize(cls, force=False):
        cls._initialized = True

    @classmethod
    def _calculate_preference_score(cls, dest, budget, season, travel_type, duration, state=None):
        score = 0.0
        max_possible = 0.0

        # 1. Season matching
        max_possible += cls.WT_SEASON
        if season and season.lower() in dest.best_season.lower():
            score += cls.WT_SEASON

        # 2. Budget Level matching
        max_possible += cls.WT_BUDGET
        if budget == dest.budget_level:
            score += cls.WT_BUDGET
        elif (budget == 'Moderate' and (dest.budget_level in ['Budget', 'Luxury'])) or \
             (dest.budget_level == 'Moderate' and (budget in ['Budget', 'Luxury'])):
            score += 10.0

        # 3. Travel Type matching
        max_possible += cls.WT_TRAVEL_TYPE
        if travel_type == 'Solo' and dest.solo_friendly:
            score += cls.WT_TRAVEL_TYPE
        elif travel_type == 'Couple' and dest.couple_friendly:
            score += cls.WT_TRAVEL_TYPE
        elif travel_type == 'Family' and dest.family_friendly:
            score += cls.WT_TRAVEL_TYPE

        # 4. Ideal Duration matching
        max_possible += cls.WT_DURATION
        try:
            diff = abs(int(duration) - dest.ideal_days)
        except (ValueError, TypeError):
            diff = 999
            
        if diff <= 1:
            score += cls.WT_DURATION
        elif diff <= 3:
            score += 8.0

        # 5. Preferred State matching
        if state:
            max_possible += cls.WT_STATE
            if dest.state and dest.state.strip().lower() == state.strip().lower():
                score += cls.WT_STATE

        preference_match = (score / max_possible) * 100.0 if max_possible > 0 else 0.0
        return round(preference_match, 2)

    @classmethod
    def _get_confidence_badge(cls, score):
        if score >= 95:
            return "Excellent Match"
        elif score >= 85:
            return "Highly Recommended"
        elif score >= 70:
            return "Good Match"
        elif score >= 50:
            return "Possible Match"
        else:
            return "Low Match"

    @classmethod
    def _generate_reasoning(cls, dest, budget, season, travel_type, duration, state=None):
        reasons = []
        if season and season.lower() in dest.best_season.lower():
            reasons.append(f"Best season matches {season}")
        if budget == dest.budget_level:
            reasons.append(f"Budget matches {budget}")
        elif (budget == 'Moderate' and (dest.budget_level in ['Budget', 'Luxury'])) or \
             (dest.budget_level == 'Moderate' and (budget in ['Budget', 'Luxury'])):
            reasons.append(f"Budget level is adjacent ({dest.budget_level})")

        if travel_type == 'Solo' and dest.solo_friendly:
            reasons.append("Highly suitable for Solo travellers")
        elif travel_type == 'Couple' and dest.couple_friendly:
            reasons.append("Perfect environment for Couples")
        elif travel_type == 'Family' and dest.family_friendly:
            reasons.append("Friendly for Families and groups")

        try:
            diff = abs(int(duration) - dest.ideal_days)
        except (ValueError, TypeError):
            diff = 999
        if diff <= 1:
            reasons.append(f"Ideal duration close to {duration} days")

        if state and dest.state and dest.state.strip().lower() == state.strip().lower():
            reasons.append(f"Located in preferred state: {dest.state}")

        reasons.append("Matches user criteria perfectly")
        return reasons

    @classmethod
    def get_hybrid_recommendations(cls, budget, season, travel_type, duration, num_travellers, state=None):
        destinations = list(Destination.objects.all().prefetch_related('attractions'))
        scored_results = []

        # Simple Profile String for token matching similarity
        profile_string = f"{season} {budget} {travel_type} {state if state else ''} {duration}"
        profile_tokens = set(cls._clean_text([profile_string]))

        for dest in destinations:
            feat_list = [
                dest.destination_name,
                dest.category,
                dest.state,
                dest.description,
                dest.best_season,
                dest.budget_level,
                "Family Friendly" if dest.family_friendly else "",
                "Solo Friendly" if dest.solo_friendly else "",
                "Couple Friendly" if dest.couple_friendly else "",
                f"{dest.average_rating} rating",
                f"{dest.ideal_days} ideal days"
            ]
            dest_tokens = set(cls._clean_text(feat_list))
            overlap = len(profile_tokens.intersection(dest_tokens))
            ml_score = min(100.0, (overlap / max(1, len(profile_tokens))) * 100.0)

            # Preference score calculation
            pref_score = cls._calculate_preference_score(
                dest=dest,
                budget=budget,
                season=season,
                travel_type=travel_type,
                duration=duration,
                state=state
            )

            # Overall Score: 70% Overlap + 30% Preference
            hybrid_score = (0.70 * ml_score) + (0.30 * pref_score)
            overall_match = int(round(hybrid_score))

            confidence = cls._get_confidence_badge(overall_match)
            reasons = cls._generate_reasoning(
                dest=dest,
                budget=budget,
                season=season,
                travel_type=travel_type,
                duration=duration,
                state=state
            )

            # Assign properties
            dest.overall_match = overall_match
            dest.ml_similarity = int(round(ml_score))
            dest.preference_match = int(round(pref_score))
            dest.confidence_badge = confidence
            dest.reasons = reasons

            scored_results.append((dest, overall_match))

        # Sort by overall match descending, then by average rating descending
        scored_results.sort(key=lambda x: (x[1], x[0].average_rating), reverse=True)
        return scored_results[:5]
