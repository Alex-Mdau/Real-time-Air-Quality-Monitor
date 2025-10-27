import time
import random
from flask import Flask, render_template, jsonify
# import requests #  Kindly Uncomment this for real API calls
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_air_quality_data_mock():
    """
    Mocks fetching real-time air quality data from an external API.
    In a real application, you would use 'requests' to hit an endpoint.
    """
    # Example coordinates around the default center (Nairobi, Kenya)
    MOCK_STATIONS = [
    {'name': 'City Centre Station', 'lat': -1.285, 'lon': 36.820, 'aqi': 55},
    {'name': 'Eastlands Monitoring', 'lat': -1.300, 'lon': 36.880, 'aqi': 120},
    {'name': 'Langata Road Sensor', 'lat': -1.350, 'lon': 36.780, 'aqi': 25},
    {'name': 'Westlands Area', 'lat': -1.265, 'lon': 36.790, 'aqi': 210},
    {'name': 'North Suburb Monitoring (Gigiri)', 'lat': -1.210, 'lon': 36.835, 'aqi': 85},
]
    # Simulate real-time updates by adding some randomness to AQI
    for station in MOCK_STATIONS:
        station['aqi'] = max(0, station['aqi'] + random.randint(-15, 15))
        station['aqi'] = min(500, station['aqi']) # Cap at max AQI
        
    # Simulate API latency
    time.sleep(0.5) 
    
    return MOCK_STATIONS

def interpret_aqi(aqi):
    """Returns the corresponding color and health text based on US EPA AQI standard."""
    if aqi <= 50:
        return {'color': '#00e400', 'level': 'Good'}
    elif aqi <= 100:
        return {'color': '#ffff00', 'level': 'Moderate'}
    elif aqi <= 150:
        return {'color': '#ff7e00', 'level': 'Unhealthy for Sensitive Groups'}
    elif aqi <= 200:
        return {'color': '#ff0000', 'level': 'Unhealthy'}
    elif aqi <= 300:
        return {'color': '#8f3f97', 'level': 'Very Unhealthy'}
    else: # > 300
        return {'color': '#7e0023', 'level': 'Hazardous'}

@app.route('/')
def index():
    """Renders the main dashboard page."""
    return render_template('index.html', config=app.config)

@app.route('/api/air_quality', methods=['GET'])
def air_quality_data():
    """API endpoint to serve air quality data to the frontend."""
    try:
        # Get data (using mock function for this example)
        station_data = get_air_quality_data_mock()
        
        # Format data for frontend, adding color and level info
        processed_data = []
        for station in station_data:
            interpretation = interpret_aqi(station['aqi'])
            processed_data.append({
                'name': station['name'],
                'lat': station['lat'],
                'lon': station['lon'],
                'aqi': station['aqi'],
                'color': interpretation['color'],
                'level': interpretation['level']
            })
            
        return jsonify({'success': True, 'stations': processed_data})
    
    except Exception as e:
        print(f"Error fetching air quality data: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch external data.'}), 500

if __name__ == '__main__':
    app.run(debug=True)