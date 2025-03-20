from flask import jsonify
from werkzeug.exceptions import HTTPException
from ..exceptions.api_exceptions import APIException


def register_error_handlers(app):
    """
    Register error handlers with the Flask application
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify({
            "status": "error",
            "message": error.message
        })
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = jsonify({
            "status": "error",
            "message": error.description
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        response = jsonify({
            "status": "error",
            "message": "An unexpected error occurred"
        })
        response.status_code = 500
        return response 