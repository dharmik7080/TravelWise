/**
 * maps/map_utils.js
 * Distance calculation, travel time estimators, and dark theme map styling definitions.
 */

/**
 * Calculates distance in kilometers between two coordinates using the Haversine formula.
 */
export function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
}

/**
 * Estimates transit duration based on distance (assuming avg city transit of 35 km/h).
 */
export function estimateTravelTime(distanceKm) {
    if (distanceKm <= 0) return "0 mins";
    // Avg speed: 35 km/h
    const hours = distanceKm / 35;
    const mins = Math.round(hours * 60);
    
    if (mins < 60) {
        return `${mins} mins`;
    }
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

/**
 * Reusable Leaflet dark-compatible basemap layer (CartoDB Dark Matter).
 */
export function getDarkTileLayer() {
    return L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    });
}
