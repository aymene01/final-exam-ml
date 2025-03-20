-- Migration: Create the tweets table

-- Use the sentiment_analysis database
USE sentiment_db;

-- Create the tweets table
CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(280) NOT NULL,
    positive TINYINT(1) NOT NULL DEFAULT 0,
    negative TINYINT(1) NOT NULL DEFAULT 0
);

-- Add comment to the table
ALTER TABLE tweets COMMENT = 'Stores tweets and their sentiment annotations';