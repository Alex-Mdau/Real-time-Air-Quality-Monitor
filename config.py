import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    TESTING = False
    AIR_QUALITY_API_KEY = os.environ.get('AQI_KEY') 
    DEFAULT_CENTER_LAT = -1.2833
    DEFAULT_CENTER_LON = 36.8167
    DEFAULT_ZOOM_LEVEL = 12