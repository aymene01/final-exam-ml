from flask import request
from flask_restx import Namespace, Resource

from ..services.sentiment_service import SentimentService
from ..schemas.request_schemas import create_tweet_list_model
from ..schemas.response_schemas import create_sentiment_response_models


# Create namespace
api = Namespace("sentiment", description="Sentiment analysis operations")

# Create request and response models
tweet_list_model = create_tweet_list_model(api)
sentiment_result_model, sentiment_response_model = create_sentiment_response_models(api)

# Create sentiment service
sentiment_service = SentimentService()


@api.route("/analyze")
class SentimentAnalysis(Resource):
    @api.doc(
        responses={
            200: "Success",
            400: "Validation Error",
            500: "Internal Server Error",
        }
    )
    @api.expect(tweet_list_model, validate=True)
    @api.marshal_with(sentiment_response_model)
    def post(self):
        """
        Analyze sentiment of a list of tweets
        Returns a sentiment score for each tweet between -1 (very negative) and 1 (very positive)
        """
        # Get tweets from request
        data = request.json
        tweets = data.get("tweets", [])
        
        if not tweets:
            api.abort(400, "No tweets provided for analysis")
        
        # Use sentiment service to analyze tweets
        results = sentiment_service.analyze_tweets(tweets)
        
        return {"results": results} 