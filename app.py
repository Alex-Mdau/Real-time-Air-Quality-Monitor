from flask import Flask, render_template, jsonify
from config import Config
from services.air_quality_service import AirQualityService, interpret_aqi

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the service with the API key from config
aq_service = AirQualityService(api_key=app.config['AIR_QUALITY_API_KEY'])

@app.route('/')
def index():
    """Renders the main dashboard page."""
    # Pass a flag to the template indicating if we are using real data
    using_real_data = bool(app.config['AIR_QUALITY_API_KEY'])
    return render_template('index.html', config=app.config, using_real_data=using_real_data)

@app.route('/api/air_quality', methods=['GET'])
def air_quality_data():
    """API endpoint to serve air quality data to the frontend."""
    try:
        # Get data using the service
        # We pass the default center coordinates, though our service currently 
        # has a hardcoded list of stations around that center.
        station_data = aq_service.get_air_quality_data(
            app.config['DEFAULT_CENTER_LAT'], 
            app.config['DEFAULT_CENTER_LON']
        )
        
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
    app.run(debug=True, host='0.0.0.0', port=5000)