//Comments are here to help understand the code better
// Global variable for the map instance
let map;
// Global variable for the layer group containing all AQI markers
let aqiMarkers = new L.LayerGroup(); 

/**
 * Initializes the Leaflet map, sets the view, and adds the tile layer.
 */
function initializeMap() {
    // Uses the coordinates passed from Flask/config.py
    map = L.map('map').setView([CONFIG.centerLat, CONFIG.centerLon], 10); 

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add the marker group to the map
    aqiMarkers.addTo(map);
    
    // Fetch and display data immediately
    fetchAQIData();
    
    // Set up a refresh interval (e.g., every 60 seconds)
    setInterval(fetchAQIData, 60000); 
}

/**
 * Fetches AQI data from the Flask backend API and updates the map markers.
 */
async function fetchAQIData() {
    console.log("Fetching real-time AQI data...");
    try {
        const response = await fetch('/api/air_quality');
        const data = await response.json();

        if (data.success && data.stations) {
            updateMapMarkers(data.stations);
        } else {
            console.error('API failed to return station data:', data.message);
        }
    } catch (error) {
        console.error('Error connecting to the backend API:', error);
    }
}

/**
 * Clears existing markers and adds new markers based on the fetched data.
 * @param {Array} stations - Array of station objects from the API.
 */
function updateMapMarkers(stations) {
    // Clear old markers from the layer group
    aqiMarkers.clearLayers(); 

    stations.forEach(station => {
        // Create a custom marker icon based on the AQI color
        const aqiIcon = L.divIcon({
            className: 'aqi-marker',
            html: `<div style="background-color: ${station.color}; border: 2px solid #333; border-radius: 50%; width: 20px; height: 20px;"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        // Create the marker
        const marker = L.marker([station.lat, station.lon], { icon: aqiIcon });

        // Create the popup content
        const popupContent = `
            <strong>Station:</strong> ${station.name}<br>
            <strong>AQI:</strong> <span style="color: ${station.color}; font-weight: bold;">${station.aqi}</span><br>
            <strong>Level:</strong> ${station.level}
        `;

        marker.bindPopup(popupContent);
        
        // Add marker to the layer group
        aqiMarkers.addLayer(marker);
    });

    console.log(`Map updated with ${stations.length} AQI stations.`);
}

// Initialize map when the script loads
document.addEventListener('DOMContentLoaded', initializeMap);