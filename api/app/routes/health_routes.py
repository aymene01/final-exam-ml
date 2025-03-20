from flask_restx import Namespace, Resource

# Create namespace
api = Namespace("health", description="Health check endpoint")


@api.route("")
class HealthCheck(Resource):
    @api.doc(
        responses={
            200: "OK - API is running",
        }
    )
    def get(self):
        """Health check endpoint to verify the API is running"""
        return {"status": "success", "message": "API is running"} 