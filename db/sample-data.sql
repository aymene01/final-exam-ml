-- Sample data for sentiment analysis training

-- Use the sentiment_analysis database
USE sentiment_db;

-- Insert sample tweets with sentiment annotations
INSERT INTO tweets (text, positive, negative) VALUES 
('I love this product! It works great.', 1, 0),
('This is the worst experience ever.', 0, 1),
('I am feeling neutral about this.', 0, 0),
('The service was excellent and fast.', 1, 0),
('Very disappointed with the quality.', 0, 1),
('Amazing customer support, thank you!', 1, 0),
('The product broke after one day.', 0, 1),
('Not bad, but could be better.', 0, 0),
('I would highly recommend this to everyone!', 1, 0),
('Never buying from this company again.', 0, 1),
('The interface is intuitive and easy to use.', 1, 0),
('Absolutely terrible customer service.', 0, 1),
('Just what I needed, perfect solution!', 1, 0),
('Waste of money, don\'t buy it.', 0, 1),
('It\'s okay, works as expected.', 0, 0);