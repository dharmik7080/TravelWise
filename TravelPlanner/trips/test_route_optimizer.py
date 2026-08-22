from django.test import TestCase
from destinations.models import Destination
from attractions.models import Attraction
from services.route_optimizer import RouteOptimizer, haversine_distance, estimate_travel_time
from services.ml.itinerary_optimizer import ItineraryOptimizer

class RouteOptimizerTestCase(TestCase):
    def setUp(self):
        # Create a test destination
        self.dest = Destination.objects.create(
            destination_name="Srinagar Test",
            city="Srinagar",
            state="Jammu & Kashmir",
            region="North",
            category="Hills",
            description="Beautiful lake city",
            best_season="Summer",
            ideal_days=3,
            budget_level="Moderate",
            average_cost_per_day=3000.0,
            family_friendly=True,
            couple_friendly=True,
            solo_friendly=True,
            average_rating=4.5
        )

        # Create test attractions with deterministic coordinates offset via MapsDataService
        self.attr1 = Attraction.objects.create(
            attraction_name="Dal Lake Test",
            destination=self.dest,
            category="Lake",
            description="Scenic lake",
            entry_fee=0.0,
            opening_time="06:00:00",
            closing_time="21:00:00",
            average_visit_time=120
        )
        self.attr2 = Attraction.objects.create(
            attraction_name="Shalimar Bagh Test",
            destination=self.dest,
            category="Garden",
            description="Mughal garden",
            entry_fee=50.0,
            opening_time="09:00:00",
            closing_time="18:00:00",
            average_visit_time=90
        )
        self.attr3 = Attraction.objects.create(
            attraction_name="Nishat Bagh Test",
            destination=self.dest,
            category="Garden",
            description="Another Mughal garden",
            entry_fee=50.0,
            opening_time="09:00:00",
            closing_time="18:00:00",
            average_visit_time=90
        )

    def test_haversine_distance_same_coords(self):
        # Same coordinates should return 0.0
        self.assertEqual(haversine_distance(34.0837, 74.7973, 34.0837, 74.7973), 0.0)

    def test_haversine_distance_valid_coords(self):
        # Distance between Srinagar and Gulmarg should be positive
        dist = haversine_distance(34.0837, 74.7973, 34.0484, 74.3805)
        self.assertGreater(dist, 0.0)

    def test_optimize_route_empty_list(self):
        opt, trans = RouteOptimizer.optimize_route([])
        self.assertEqual(opt, [])
        self.assertEqual(trans, [])

    def test_optimize_route_one_attraction(self):
        opt, trans = RouteOptimizer.optimize_route([self.attr1])
        self.assertEqual(opt, [self.attr1])
        self.assertEqual(trans, [])

    def test_optimize_route_multiple_attractions(self):
        # Optimize Dal Lake, Shalimar Bagh, Nishat Bagh
        opt, trans = RouteOptimizer.optimize_route([self.attr1, self.attr2, self.attr3])
        self.assertEqual(len(opt), 3)
        self.assertEqual(len(trans), 2)
        # Check no duplicates
        self.assertEqual(len(set(opt)), 3)

    def test_optimize_route_missing_coordinates(self):
        # We can construct a mock attraction without destination (or standard behavior fallback)
        # Let's mock a coordinate lookup failure in a dummy attraction
        class DummyAttraction:
            def __init__(self, pk, name):
                self.pk = pk
                self.attraction_name = name
                self.destination = None  # Causes coordinate resolution exception

        dummy = DummyAttraction(999, "No Coords Spot")
        opt, trans = RouteOptimizer.optimize_route([self.attr1, dummy])
        self.assertIn(dummy, opt)
        # Coords-less item should be appended at the end of the optimized list
        self.assertEqual(opt[-1], dummy)

    def test_itinerary_optimization_multiple_days(self):
        # Generate an itinerary for 2 days
        itinerary = ItineraryOptimizer.optimize(
            destination=self.dest,
            total_days=2,
            travel_type="Solo",
            budget_level="Moderate"
        )
        self.assertEqual(len(itinerary), 2)
        # Verify both days exist and are optimized independently
        self.assertIn(1, itinerary)
        self.assertIn(2, itinerary)

    def test_itinerary_regeneration_works(self):
        # Test that regeneration flag generates a valid itinerary
        itinerary = ItineraryOptimizer.optimize(
            destination=self.dest,
            total_days=1,
            travel_type="Solo",
            budget_level="Moderate",
            regenerate=True
        )
        self.assertIn(1, itinerary)
