from flask import Flask
from .config import config_by_name
from .routes.route_registry import register_routes
from .utils.error_handlers import register_error_handlers


def create_app(config_name="dev"):
    """
    Create and configure the Flask application
    
    Args:
        config_name: Configuration environment (dev, test, prod)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions (DB, etc) here
    # This will be implemented with DB connection later
    
    # Register all routes
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app 