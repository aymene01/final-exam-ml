from flask_restx import fields

def create_sentiment_response_models(api):
    """
    Create models for sentiment analysis response validation
    
    Args:
        api: Flask-RestX API instance
        
    Returns:
        Tuple of (sentiment_result_model, sentiment_response_model)
    """
    sentiment_result_model = api.model(
        "SentimentResult",
        {
            "tweet": fields.String(description="The analyzed tweet"),
            "score": fields.Float(
                description="Sentiment score from -1 (very negative) to 1 (very positive)"
            ),
        },
    )

    sentiment_response_model = api.model(
        "SentimentResponse",
        {
            "results": fields.List(
                fields.Nested(sentiment_result_model),
                description="List of sentiment analysis results",
            ),
        },
    )
    
    return sentiment_result_model, sentiment_response_model 