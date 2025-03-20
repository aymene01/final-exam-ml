from flask import Blueprint
from flask_restx import Api

# Import namespaces
from .health_routes import api as health_ns
from .sentiment_routes import api as sentiment_ns


def register_routes(app):
    """
    Register all API routes with the Flask application
    
    Args:
        app: Flask application instance
    """
    # Create main API blueprint
    api_v1_blueprint = Blueprint("api_v1", __name__)
    
    # Register the blueprint with the app
    app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")
    
    # Create API documentation with a version compatible with the current flask-restx
    api = Api(
        app, 
        title="SocialMetrics AI Sentiment Analysis API",
        version="1.0",
        description="API for sentiment analysis of tweets",
        doc="/docs"
    )
    
    # Add namespaces to the API
    api.add_namespace(health_ns)
    api.add_namespace(sentiment_ns)
    
    return api 