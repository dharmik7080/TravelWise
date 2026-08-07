/**
 * maps/marker_manager.js
 * Handles SVG icon generation, marker binding, popups, and radius overlays.
 */
import { calculateHaversineDistance } from './map_utils.js';

// Hex codes mapping for color consistency (Step 6)
const MARKER_COLORS = {
    'destination': '#0d6efd', // Blue
    'morning': '#ffc107',     // Yellow
    'afternoon': '#fd7e14',   // Orange
    'evening': '#6f42c1',     // Purple
    'hotel': '#198754',       // Green
    'similar': '#0dcaf0'      // Cyan (similar destinations)
};

/**
 * Constructs a custom Leaflet DivIcon utilizing custom SVG pins.
 */
export function createCustomIcon(type) {
    const color = MARKER_COLORS[type.toLowerCase()] || '#6c757d';
    const svgHtml = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" style="filter: drop-shadow(0px 3px 3px rgba(0,0,0,0.3));">
            <path fill="${color}" stroke="#ffffff" stroke-width="1.5" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
        </svg>
    `;
    return L.divIcon({
        html: svgHtml,
        className: 'custom-map-marker',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
}

/**
 * Binds click actions to highlight nearby attractions within a 5 km circle overlay (Step 10).
 */
export function registerNearbyHighlighting(map, activeMarker, activeAttr, allAttractionMarkers) {
    let currentCircle = null;

    activeMarker.on('click', () => {
        // Remove existing circle if drawn
        if (currentCircle) {
            map.removeLayer(currentCircle);
        }

        // Draw 5 km radius circle (5000 meters) around clicked marker
        currentCircle = L.circle(activeMarker.getLatLng(), {
            color: '#0dcaf0',
            fillColor: '#0dcaf0',
            fillOpacity: 0.15,
            radius: 5000, // 5 km
            weight: 1.5
        }).addTo(map);

        // Highlight attractions within 5 km, fade out others
        allAttractionMarkers.forEach(m => {
            const dist = calculateHaversineDistance(
                activeAttr.lat, activeAttr.lon,
                m.options.lat, m.options.lon
            );

            if (dist <= 5.0) {
                m.setOpacity(1.0); // Full opacity for nearby
            } else {
                m.setOpacity(0.4); // Fade out far ones
            }
        });
    });

    // Reset opacity when map is clicked elsewhere
    map.on('click', (e) => {
        if (e.originalEvent.target.tagName !== 'path' && e.originalEvent.target.tagName !== 'svg') {
            if (currentCircle) {
                map.removeLayer(currentCircle);
                currentCircle = null;
            }
            allAttractionMarkers.forEach(m => m.setOpacity(1.0));
        }
    });
}
