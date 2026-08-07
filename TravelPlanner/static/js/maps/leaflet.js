/**
 * maps/leaflet.js
 * Lazy-loader class for Leaflet and MarkerCluster script/style assets.
 */
export class LeafletLoader {
    static load() {
        if (this._promise) {
            return this._promise;
        }

        this._promise = new Promise((resolve, reject) => {
            // Check if already loaded globally
            if (typeof L !== 'undefined' && typeof L.markerClusterGroup !== 'undefined') {
                resolve();
                return;
            }

            // 1. Append Leaflet base CSS
            if (!document.querySelector('link[href*="leaflet.css"]')) {
                const link = document.createElement('link');
                link.rel = 'stylesheet';
                link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
                link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';
                link.crossOrigin = '';
                document.head.appendChild(link);
            }

            // 2. Append Marker Cluster CSS
            if (!document.querySelector('link[href*="MarkerCluster.css"]')) {
                const clusterCSS = document.createElement('link');
                clusterCSS.rel = 'stylesheet';
                clusterCSS.href = 'https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css';
                document.head.appendChild(clusterCSS);

                const clusterThemeCSS = document.createElement('link');
                clusterThemeCSS.rel = 'stylesheet';
                clusterThemeCSS.href = 'https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css';
                document.head.appendChild(clusterThemeCSS);
            }

            // 3. Append Leaflet JS
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
            script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
            script.crossOrigin = '';
            
            script.onload = () => {
                // 4. Append Marker Cluster JS after core Leaflet is ready
                const clusterScript = document.createElement('script');
                clusterScript.src = 'https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js';
                clusterScript.onload = () => {
                    resolve();
                };
                clusterScript.onerror = () => reject(new Error('Failed to load Leaflet MarkerCluster'));
                document.body.appendChild(clusterScript);
            };

            script.onerror = () => reject(new Error('Failed to load Leaflet core JS'));
            document.body.appendChild(script);
        });

        return this._promise;
    }
}
