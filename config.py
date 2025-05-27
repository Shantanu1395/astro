import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application settings
    APP_NAME = "Vedic Astrology Prediction System"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Default location for calculations (can be overridden by user input)
    DEFAULT_TIMEZONE = "UTC"

    # Vedic astrology specific settings
    AYANAMSA = "LAHIRI"  # Default ayanamsa for sidereal calculations

    # ===== LLM PROVIDER CONFIGURATION =====
    # Options: "openai", "ollama", "fallback"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1500"))
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "60"))

    # Ollama Configuration
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "codestral")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

    # Backward compatibility
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7

config = Config()
