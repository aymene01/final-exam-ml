-- init.sql
-- Master initialization file that runs all migrations in order

-- Use the sentiment_analysis database
USE sentiment_db;

-- Run migration 1: Create tweets table
SOURCE /docker-entrypoint-initdb.d/migrations/001_create_tweets_table.sql;

-- Run migration 2: Add indexes
SOURCE /docker-entrypoint-initdb.d/migrations/002_add_indexes.sql;

-- Run migration 3: Add timestamps
SOURCE /docker-entrypoint-initdb.d/migrations/003_add_timestamps.sql;