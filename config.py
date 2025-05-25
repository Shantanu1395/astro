import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Application settings
    APP_NAME = "Vedic Astrology Prediction System"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Default location for calculations (can be overridden by user input)
    DEFAULT_TIMEZONE = "UTC"
    
    # Vedic astrology specific settings
    AYANAMSA = "LAHIRI"  # Default ayanamsa for sidereal calculations
    
    # LLM settings
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7

config = Config()
