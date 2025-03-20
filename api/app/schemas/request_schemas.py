from flask_restx import fields

def create_tweet_list_model(api):
    """
    Create the model for tweet list request validation
    
    Args:
        api: Flask-RestX API instance
        
    Returns:
        Model for tweet list validation
    """
    return api.model(
        "TweetList",
        {
            "tweets": fields.List(
                fields.String(description="Tweet content"),
                required=True,
                description="List of tweets to analyze",
            ),
        },
    ) 