import math
import os
import sys

# Ensure parent directory is in path
services_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(services_dir)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from services.maps_data_service import MapsDataService

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the approximate distance between two coordinates in kilometers.
    """
    if None in (lat1, lon1, lat2, lon2):
        return 0.0
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def estimate_travel_time(distance_km, average_speed_kmh=40.0):
    """
    Estimates travel time in minutes based on distance and average speed (default 40 km/h).
    """
    if distance_km <= 0:
        return 0
    hours = distance_km / average_speed_kmh
    return int(round(hours * 60.0))

class RouteOptimizer:
    """
    Geospatial Route Optimization service using the Nearest Neighbor heuristic.
    """

    @classmethod
    def optimize_route(cls, attractions, start_coords=None):
        """
        Orders attractions geographically using Nearest Neighbor heuristic to reduce travel distance.
        Returns a tuple of (ordered_attractions, transitions_metadata).
        """
        if not attractions:
            return [], []

        has_coords = []
        no_coords = []
        coords_cache = {}

        for attr in attractions:
            try:
                # Resolve coordinates
                d_lat, d_lon = MapsDataService.get_destination_coords(attr.destination)
                lat, lon = MapsDataService.get_attraction_coords(d_lat, d_lon, attr.attraction_name)
                if lat is not None and lon is not None:
                    has_coords.append(attr)
                    coords_cache[attr.pk] = (lat, lon)
                else:
                    no_coords.append(attr)
            except Exception:
                no_coords.append(attr)

        if not has_coords:
            # Fallback if no coordinates are available
            return list(attractions), []

        optimized = []
        unvisited = list(has_coords)

        # Starting point determination
        current_coords = start_coords
        if current_coords is None:
            # Default to starting at the first attraction
            first_attr = unvisited.pop(0)
            optimized.append(first_attr)
            current_coords = coords_cache[first_attr.pk]

        # Cache distances to avoid redundant calculations
        distance_memo = {}
        def get_distance(pk1, pk2):
            key = tuple(sorted((pk1, pk2)))
            if key not in distance_memo:
                c1 = coords_cache[pk1]
                c2 = coords_cache[pk2]
                distance_memo[key] = haversine_distance(c1[0], c1[1], c2[0], c2[1])
            return distance_memo[key]

        while unvisited:
            closest_attr = None
            min_dist = float('inf')
            
            for attr in unvisited:
                c = coords_cache[attr.pk]
                dist = haversine_distance(current_coords[0], current_coords[1], c[0], c[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_attr = attr

            unvisited.remove(closest_attr)
            optimized.append(closest_attr)
            current_coords = coords_cache[closest_attr.pk]

        # Add coordinate-less attractions at the end to keep them in the itinerary
        optimized.extend(no_coords)

        # Calculate transit steps (transitions)
        transitions = []
        for i in range(len(optimized) - 1):
            attr1 = optimized[i]
            attr2 = optimized[i+1]
            if attr1.pk in coords_cache and attr2.pk in coords_cache:
                dist = get_distance(attr1.pk, attr2.pk)
                time_min = estimate_travel_time(dist)
            else:
                dist = 0.0
                time_min = 0

            transitions.append({
                'from_id': attr1.pk,
                'to_id': attr2.pk,
                'distance_km': round(dist, 1),
                'travel_time_min': time_min
            })

        return optimized, transitions
