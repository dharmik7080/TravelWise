import hashlib

class MapsDataService:
    """
    Service supplying coordinates mapping and deterministic offsets
    for destinations and their attractions.
    """
    # Coordinates map for known Indian cities/destinations
    COORDINATES = {
        'srinagar': [34.0837, 74.7973],
        'gulmarg': [34.0484, 74.3805],
        'pahalgam': [34.0161, 75.3150],
        'leh': [34.1526, 77.5771],
        'manali': [32.2396, 77.1887],
        'shimla': [31.1048, 77.1734],
        'dharamshala': [32.2190, 76.3234],
        'dalhousie': [32.5387, 75.9710],
        'mussoorie': [30.4599, 78.0664],
        'nainital': [29.3803, 79.4636],
        'rishikesh': [30.0869, 78.2676],
        'haridwar': [29.9457, 78.1642],
        'auli': [30.5283, 79.5694],
        'jaipur': [26.9124, 75.7873],
        'udaipur': [24.5854, 73.7125],
        'jodhpur': [26.2389, 73.0243],
        'jaisalmer': [26.9157, 70.9083],
        'pushkar': [26.4897, 74.5511],
        'ranthambore': [25.8667, 76.3000],
        'agra': [27.1767, 78.0081],
        'varanasi': [25.3176, 82.9739],
        'ooty': [11.4102, 76.6950],
        'munnar': [10.0889, 77.0595],
        'alleppey': [9.4981, 76.3388],
        'kochi': [9.9312, 76.2673],
        'hampi': [15.3350, 76.4600],
        'mysore': [12.2958, 76.6394],
        'amritsar': [31.6340, 74.8723],
        'goa': [15.4909, 73.8278],
        'panaji': [15.4909, 73.8278],
    }

    @classmethod
    def get_destination_coords(cls, dest):
        """
        Retrieves [lat, lon] coordinates for a destination object.
        """
        if not dest:
            return [20.5937, 78.9629] # Center of India fallback
        
        city_key = dest.city.strip().lower() if dest.city else ""
        name_key = dest.destination_name.strip().lower() if dest.destination_name else ""

        if city_key in cls.COORDINATES:
            return cls.COORDINATES[city_key]
        if name_key in cls.COORDINATES:
            return cls.COORDINATES[name_key]
        
        # Fallback to a deterministic coordinate based on the destination name/ID hash
        h = int(hashlib.md5(dest.destination_name.encode('utf-8')).hexdigest(), 16)
        # Random but deterministic spot in India (lat: 12 to 28, lon: 73 to 84)
        lat = 12.0 + (h % 1600) / 100.0
        lon = 73.0 + ((h // 1600) % 1100) / 100.0
        return [lat, lon]

    @classmethod
    def get_attraction_coords(cls, parent_lat, parent_lon, attr_name):
        """
        Derives stable, deterministic coordinate offsets for attractions near their parent center.
        """
        h = int(hashlib.md5(attr_name.encode('utf-8')).hexdigest(), 16)
        # Offset within ~5 km radius (approx 0.03 degrees max)
        lat_offset = ((h % 200) - 100) / 3300.0
        lon_offset = (((h // 200) % 200) - 100) / 3300.0
        return [parent_lat + lat_offset, parent_lon + lon_offset]
