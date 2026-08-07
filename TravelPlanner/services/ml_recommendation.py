import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from destinations.models import Destination

class MLRecommendationService:
    # Preference weights (Task 5 constants)
    WT_SEASON = 25.0
    WT_BUDGET = 25.0
    WT_TRAVEL_TYPE = 20.0
    WT_DURATION = 15.0
    WT_STATE = 15.0

    # In-memory caching for performance (Task 10)
    _vectorizer = None
    _tfidf_matrix = None
    _destination_ids = []
    _destinations_cache = {}
    _initialized = False

    @classmethod
    def _clean_text(cls, features_list):
        """
        Cleans text features: lowercase, removes duplicates, removes non-alphanumeric.
        """
        cleaned_words = []
        for feat in features_list:
            if not feat:
                continue
            # Tokenize words using alphanumeric regex, lowercase them
            words = re.findall(r'\b\w+\b', str(feat).lower())
            cleaned_words.extend(words)
            
        # Remove duplicates while preserving insertion order
        unique_words = list(dict.fromkeys(cleaned_words))
        return " ".join(unique_words)

    @classmethod
    def _initialize(cls, force=False):
        """
        Loads and vectorizes all Destination data, prefetching associated attractions.
        """
        if cls._initialized and not force:
            return

        destinations = list(Destination.objects.all().prefetch_related('attractions'))
        
        feature_strings = []
        cls._destination_ids = []
        cls._destinations_cache = {}

        for dest in destinations:
            # Step 1: Feature Engineering
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

            # Append attraction details as travel tags
            for attr in dest.attractions.all():
                feat_list.extend([attr.attraction_name, attr.category, attr.description])

            cleaned_str = cls._clean_text(feat_list)
            feature_strings.append(cleaned_str)
            cls._destination_ids.append(dest.pk)
            cls._destinations_cache[dest.pk] = dest

        if not feature_strings:
            return

        # Step 2: TF-IDF Vectorization
        cls._vectorizer = TfidfVectorizer()
        cls._tfidf_matrix = cls._vectorizer.fit_transform(feature_strings)
        cls._initialized = True

    @classmethod
    def _calculate_preference_score(cls, dest, budget, season, travel_type, duration, state=None):
        """
        Calculates simple rule-based preference score normalized to 0-100.
        """
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
            score += 10.0  # Partial match weight

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
            score += 8.0  # Partial match weight

        # 5. Preferred State matching
        if state:
            max_possible += cls.WT_STATE
            if dest.state and dest.state.strip().lower() == state.strip().lower():
                score += cls.WT_STATE

        preference_match = (score / max_possible) * 100.0 if max_possible > 0 else 0.0
        return round(preference_match, 2)

    @classmethod
    def _get_confidence_badge(cls, score):
        """
        Maps score to standard confidence level badges.
        """
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
        """
        Compiles list of explanation statements for explainable AI.
        """
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

        reasons.append("Similar destinations frequently share these characteristics")
        return reasons

    @classmethod
    def get_hybrid_recommendations(cls, budget, season, travel_type, duration, num_travellers, state=None):
        """
        Computes Hybrid Content-Based (TF-IDF + Cosine Similarity) and Preference recommendations.
        Returns top 5 sorted results list: (destination, overall_match).
        """
        # Ensure model is initialized
        cls._initialize()

        if not cls._initialized:
            # Fallback to basic DB list if model has no data
            return []

        # Step 3: User Profile Vector
        user_features = [
            season,
            budget,
            travel_type,
            state if state else "",
            f"{duration} Days"
        ]
        user_string = cls._clean_text(user_features)
        user_vector = cls._vectorizer.transform([user_string])

        # Step 4: Cosine Similarity
        ml_similarities = cosine_similarity(user_vector, cls._tfidf_matrix).flatten()
        max_sim = np.max(ml_similarities)

        scored_results = []
        for idx, dest_id in enumerate(cls._destination_ids):
            dest = cls._destinations_cache.get(dest_id)
            if not dest:
                continue

            # Normalized ML similarity score (0-100) relative to maximum match
            sim_score = float(ml_similarities[idx])
            ml_score = (sim_score / max_sim) * 100.0 if max_sim > 0 else 0.0

            # Step 5: Preference Score
            pref_score = cls._calculate_preference_score(
                dest=dest,
                budget=budget,
                season=season,
                travel_type=travel_type,
                duration=duration,
                state=state
            )

            # Step 6: Hybrid Scoring (70% ML Similarity + 30% Preference Score)
            hybrid_score = (0.70 * ml_score) + (0.30 * pref_score)
            overall_match = int(round(hybrid_score))

            # Step 7: Explainable AI details
            confidence = cls._get_confidence_badge(overall_match)
            reasons = cls._generate_reasoning(
                dest=dest,
                budget=budget,
                season=season,
                travel_type=travel_type,
                duration=duration,
                state=state
            )

            # Attach stats directly to Destination object
            dest.overall_match = overall_match
            dest.ml_similarity = int(round(ml_score))
            dest.preference_match = int(round(pref_score))
            dest.confidence_badge = confidence
            dest.reasons = reasons

            scored_results.append((dest, overall_match))

        # Sort by overall match descending, then by average rating descending
        scored_results.sort(key=lambda x: (x[1], x[0].average_rating), reverse=True)
        return scored_results[:5]
