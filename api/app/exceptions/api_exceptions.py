class APIException(Exception):
    """Base exception for API errors"""
    
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(APIException):
    """Exception raised for validation errors"""
    
    def __init__(self, message):
        super().__init__(message, status_code=400)


class ResourceNotFoundError(APIException):
    """Exception raised when a resource is not found"""
    
    def __init__(self, message):
        super().__init__(message, status_code=404)


class DatabaseError(APIException):
    """Exception raised for database errors"""
    
    def __init__(self, message):
        super().__init__(message, status_code=500)


class ModelError(APIException):
    """Exception raised for ML model errors"""
    
    def __init__(self, message):
        super().__init__(message, status_code=500) 