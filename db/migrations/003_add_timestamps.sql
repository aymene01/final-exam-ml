-- Migration: Add timestamp columns to tweets table

-- Use the sentiment_analysis database
USE sentiment_db;

-- Add timestamp columns
ALTER TABLE tweets 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Create index on created_at for time-based queries
CREATE INDEX idx_created_at ON tweets(created_at);