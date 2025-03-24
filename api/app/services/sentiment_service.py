from typing import Dict, List, Any
from ..utils.logger import logger
import boto3
from botocore.config import Config
import os
import joblib
import re
import tempfile
import time
from botocore.exceptions import ClientError


class SentimentService:
    """Service for analyzing sentiment in tweets"""
    
    def __init__(self):
        """Initialize the sentiment service"""
        self.model = None
        self.vectorizer = None
        self._load_models_from_minio_with_retry()
        logger.info("Sentiment service initialized")
        
    def _load_models_from_minio_with_retry(self, max_retries=5, delay=10):
        """Load the trained model and vectorizer from MinIO with retries"""
        for attempt in range(max_retries):
            try:
                self._load_models_from_minio()
                return
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    logger.warning(f"Models not found in MinIO, attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        logger.info(f"Waiting {delay} seconds before next attempt...")
                        time.sleep(delay)
                        continue
                    raise RuntimeError("Models not found in MinIO after maximum retries")
                raise
            except Exception as e:
                logger.error(f"Unexpected error loading models: {e}")
                raise

    def _load_models_from_minio(self):
        """Load the trained model and vectorizer from MinIO"""
        try:
            # Initialize MinIO client
            s3_client = boto3.client(
                's3',
                endpoint_url=os.environ.get('MINIO_ENDPOINT_URL', 'http://minio:9000'),
                aws_access_key_id=os.environ.get('MINIO_ACCESS_KEY', 'minioadmin'),
                aws_secret_access_key=os.environ.get('MINIO_SECRET_KEY', 'minioadmin'),
                config=Config(signature_version='s3v4'),
                region_name=os.environ.get('MINIO_REGION_NAME', 'us-east-1')
            )

            # Create temporary files to store the downloaded models
            with tempfile.NamedTemporaryFile() as model_temp, tempfile.NamedTemporaryFile() as vectorizer_temp:
                # Download files from MinIO
                s3_client.download_file('ml-models', 'trained_model.joblib', model_temp.name)
                s3_client.download_file('ml-models', 'vectorizer.joblib', vectorizer_temp.name)
                
                # Load the models
                self.model = joblib.load(model_temp.name)
                self.vectorizer = joblib.load(vectorizer_temp.name)
                
            logger.info("Successfully loaded model and vectorizer from MinIO")
        except Exception as e:
            logger.error(f"Error loading models from MinIO: {e}")
            raise

    def _clean_text(self, text: str) -> str:
        """Clean the text using the same method as training"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = ' '.join(text.split())
        return text

    def analyze_tweets(self, tweets: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze the sentiment of a list of tweets
        
        Args:
            tweets: List of tweet texts to analyze
            
        Returns:
            List of dictionaries containing analyzed tweets and their sentiment scores
        """
        logger.info(f"Analyzing sentiment for {len(tweets)} tweets")
        
        # Clean tweets
        cleaned_tweets = [self._clean_text(tweet) for tweet in tweets]
        
        # Vectorize tweets
        vectorized_tweets = self.vectorizer.transform(cleaned_tweets)
        
        # Get predictions and probabilities
        predictions = self.model.predict(vectorized_tweets)
        probabilities = self.model.predict_proba(vectorized_tweets)
        
        # Convert predictions to scores using probabilities
        results = []
        for tweet, pred, proba in zip(tweets, predictions, probabilities):
            score = proba[1] if pred == 1 else -proba[0]
            results.append({
                "tweet": tweet,
                "score": float(score),

            })
            
        return results 