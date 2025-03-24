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
        self.user = user or os.environ.get('DB_USER', 'user')
        self.password = password or os.environ.get('DB_PASSWORD', 'password')
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
        """Fetch data from the last 7 days"""
        try:
            connection = self.connect()
            if not connection:
                return None
                
            cursor = connection.cursor(dictionary=True)
            
            # Query to get data from the last 7 days
            query = """
                SELECT id, text, positive, negative, created_at 
                FROM tweets 
                WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            """
            cursor.execute(query)
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