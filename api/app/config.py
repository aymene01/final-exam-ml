import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "sentiment_db")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # API settings
    API_TITLE = "SocialMetrics AI Sentiment Analysis API"
    API_VERSION = "1.0"
    
    # Model settings
    MODEL_PATH = os.path.join(os.getcwd(), "models")


class DevelopmentConfig(Config):
    """Development configuration class"""
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    """Testing configuration class"""
    DEBUG = True
    TESTING = True
    ENV = "testing"
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration class"""
    DEBUG = False
    ENV = "production"
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())


# Export configuration dictionary
config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
} 