import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class DatabaseOperations:
    def __init__(self, host=None, user=None, password=None, database=None):
        """Initialize database connection parameters"""
        self.host = host or os.environ.get('DB_HOST', 'localhost')
        self.user = user or os.environ.get('DB_USER', 'sentiment_user')
        self.password = password or os.environ.get('DB_PASSWORD', 'sentiment_password')
        self.database = database or os.environ.get('DB_NAME', 'sentiment_db')
        self.connection = None
    
    def connect(self):
        """Create a database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def fetch_last_7_days_data(self):
        """Fetch training data from the last 7 days"""
        try:
            connection = self.connect()
            if not connection:
                return None
                
            cursor = connection.cursor(dictionary=True)
            
            # Calculate date 7 days ago from today
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # Query to get tweets from the last 7 days
            query = """
                SELECT id, text, positive, negative, created_at 
                FROM tweets 
                WHERE created_at >= %s
                ORDER BY created_at DESC
            """
            
            cursor.execute(query, (seven_days_ago,))
            results = cursor.fetchall()
            
            if not results:
                print("No data found in the last 7 days")
                return []
            
            return results
            
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            self.disconnect()

    def fetch_all_training_data(self):
        """Fetch all training data from the database"""
        try:
            connection = self.connect()
            if not connection:
                return None
                
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all tweets
            query = "SELECT id, text, positive, negative, created_at FROM tweets"
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                print("No data found in the database")
                return []
                
            return results
            
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            self.disconnect()
    
    def save_tweet(self, text: str, positive: int, negative: int) -> bool:
        """Save a new tweet with sentiment labels"""
        try:
            connection = self.connect()
            if not connection:
                return False
                
            cursor = connection.cursor()
            
            query = """
                INSERT INTO tweets (text, positive, negative) 
                VALUES (%s, %s, %s)
            """
            
            cursor.execute(query, (text, positive, negative))
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error saving tweet: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.disconnect()
            
    def save_multiple_tweets(self, tweets_data: List[Dict]) -> bool:
        """Save multiple tweets with their sentiment values"""
        try:
            connection = self.connect()
            if not connection:
                return False
                
            cursor = connection.cursor()
            
            query = """
                INSERT INTO tweets (text, positive, negative) 
                VALUES (%s, %s, %s)
            """
            
            data = [(t['text'], t['positive'], t['negative']) for t in tweets_data]
            cursor.executemany(query, data)
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error saving tweets: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            self.disconnect()


def test_db_operations():
    db_ops = DatabaseOperations()
    df = db_ops.fetch_last_7_days_data()
    print(type(df))
    if df is not None:
        for element in df:
            print(element)
        print(f"Successfully retrieved {len(df)} records from the last 7 days")
        return True
    else:
        print("Failed to retrieve data from the last 7 days")
        return False

if __name__ == "__main__":
    test_db_operations() 