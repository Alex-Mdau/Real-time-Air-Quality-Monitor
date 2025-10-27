import os

class Config:
    """Base configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') #Use your own key
    DEBUG = True
    TESTING = False
    # Example API key for this example air quality again use your own
    AIR_QUALITY_API_KEY = os.environ.get('AQI_KEY') 
    DEFAULT_CENTER_LAT = -1.2833
    DEFAULT_CENTER_LON = 36.8167
    DEFAULT_ZOOM_LEVEL = 12