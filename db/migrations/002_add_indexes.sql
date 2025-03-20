-- Migration: Add indexes to tweets table for better performance

-- Use the sentiment_analysis database
USE sentiment_db;

-- Create indexes for faster querying
CREATE INDEX idx_positive ON tweets(positive);
CREATE INDEX idx_negative ON tweets(negative);