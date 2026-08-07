/**
 * maps/route_renderer.js
 * Handles drawing, re-rendering, and distance totaling for daily travel routes.
 */
import { calculateHaversineDistance, estimateTravelTime } from './map_utils.js';

// Color mappings for different day routes
const DAY_ROUTE_COLORS = {
    1: '#0ea5e9', // Day 1: Sky Blue
    2: '#10b981', // Day 2: Emerald Green
    3: '#f59e0b', // Day 3: Amber
    4: '#ec4899', // Day 4: Pink
    5: '#8b5cf6'  // Day 5: Purple
};

/**
 * Draws polylines and markers for the itinerary, computing distances.
 */
export class RouteRenderer {
    constructor(map) {
        this.map = map;
        this.routeLayers = {};
    }

    /**
     * Renders daily routes connecting morning -> afternoon -> evening.
     */
    renderRoutes(itineraryDaysData, markerManager) {
        // Clear any old layers first
        Object.values(this.routeLayers).forEach(layerGroup => {
            this.map.removeLayer(layerGroup);
        });
        this.routeLayers = {};

        const allLatLngs = [];
        let totalDistance = 0.0;
        let routeHtml = '<ul class="list-unstyled mb-0 d-flex flex-column gap-2">';

        Object.keys(itineraryDaysData).forEach(dayNum => {
            const dayData = itineraryDaysData[dayNum];
            const slots = ['morning', 'afternoon', 'evening'];
            const latLngs = [];
            const dayGroup = L.layerGroup();
            
            let dayDistance = 0.0;
            let lastCoord = null;

            slots.forEach(slot => {
                const item = dayData[slot];
                if (item && item.lat && item.lon) {
                    const coord = [item.lat, item.lon];
                    latLngs.append ? latLngs.push(coord) : latLngs.push(coord);
                    allLatLngs.push(coord);

                    // Create marker for slot
                    const markerIcon = markerManager.createCustomIcon(slot);
                    const marker = L.marker(coord, { 
                        icon: markerIcon,
                        lat: item.lat,
                        lon: item.lon 
                    });
                    
                    marker.bindPopup(`
                        <div style="font-family: 'Poppins', sans-serif;">
                            <strong class="text-primary d-block">${item.name}</strong>
                            <span class="badge bg-secondary mb-1">${slot.toUpperCase()}</span><br>
                            <span class="small text-muted">Category: ${item.category || 'Sightseeing'}</span>
                        </div>
                    `);
                    
                    marker.addTo(dayGroup);

                    // Add distance
                    if (lastCoord) {
                        const dist = calculateHaversineDistance(
                            lastCoord[0], lastCoord[1],
                            coord[0], coord[1]
                        );
                        dayDistance += dist;
                    }
                    lastCoord = coord;
                }
            });

            // Draw polyline connecting stops if there are at least 2 stops
            if (latLngs.length >= 2) {
                const color = DAY_ROUTE_COLORS[dayNum] || '#6c757d';
                const polyline = L.polyline(latLngs, {
                    color: color,
                    weight: 3.5,
                    opacity: 0.8,
                    dashArray: '5, 8'
                });
                polyline.addTo(dayGroup);
            }

            dayGroup.addTo(this.map);
            this.routeLayers[dayNum] = dayGroup;

            totalDistance += dayDistance;
            const dayTime = estimateTravelTime(dayDistance);
            routeHtml += `
                <li class="d-flex justify-content-between border-bottom pb-1" style="border-color: rgba(255,255,255,0.05) !important;">
                    <span class="text-white fw-semibold">Day ${dayNum}</span>
                    <span class="text-secondary font-monospace">Est. Distance: ${dayDistance.toFixed(1)} km (${dayTime} transit)</span>
                </li>
            `;
        });

        routeHtml += '</ul>';

        // Update the route summary container in the HTML
        const summaryDiv = document.getElementById('distance-details');
        if (summaryDiv) {
            const overallTime = estimateTravelTime(totalDistance);
            summaryDiv.innerHTML = `
                <div class="mb-2 text-white fw-bold">Total Route Distance: ${totalDistance.toFixed(1)} km (~${overallTime} total travel)</div>
                ${routeHtml}
            `;
        }

        // Fit map bounds to show all path lines (Step 4)
        if (allLatLngs.length > 0) {
            this.map.fitBounds(allLatLngs, { padding: [40, 40] });
        }
    }

    /**
     * Toggles visibility of a specific day's route layers (Step 5 toggle).
     */
    filterDay(activeDay) {
        Object.keys(this.routeLayers).forEach(dayNum => {
            const layerGroup = this.routeLayers[dayNum];
            if (activeDay === 'all' || activeDay === dayNum) {
                this.map.addLayer(layerGroup);
            } else {
                this.map.removeLayer(layerGroup);
            }
        });
    }
}
