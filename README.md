# Sentiment Analysis Project with Machine Learning

This project is a sentiment analysis application that uses machine learning to classify tweets as positive or negative.

## Project Architecture

The project consists of three main services:

1. **API (Flask)**
   - REST service for sentiment analysis
   - `/analyze` endpoint for analyzing tweets
   - Results storage in MySQL

2. **ML Service**
   - Weekly model training
   - Using scikit-learn (LogisticRegression)
   - Model storage in MinIO

3. **Database**
   - MySQL for storing tweets and annotations
   - MinIO for storing ML models

## Directory Structure

```
.
├── api/                    # API Service
│   ├── app/
│   │   ├── routes/        # API Routes
│   │   ├── services/      # Business Services
│   │   ├── schemas/       # Request/Response Schemas
│   │   ├── models/        # Database Models
│   │   ├── exceptions/    # Custom Exceptions
│   │   ├── config/        # Configuration Files
│   │   └── utils/         # Utilities
│   └── Dockerfile
├── ml/                     # ML Service
│   ├── utils/             # Utilities
│   └── train.py           # Training Script
├── db/                     # Database Scripts
│   ├── migrations/        # Database Migrations
│   └── sample-data.sql    # Sample Data
└── docker-compose.yml      # Docker Configuration
```

## Technologies Used

- Python 3.9+
- Flask
- scikit-learn
- MySQL
- MinIO
- Docker & Docker Compose

## Installation and Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Start services with Docker Compose:
```bash
docker compose up -d
```

The following services will be started:
- API: http://localhost:5000
- MinIO: http://localhost:9000
- MySQL: localhost:3306

## API Usage

### Sentiment Analysis Endpoint

```bash
POST /analyze
Content-Type: application/json

{
    "tweets": [
        "I love this product!",
        "This is terrible.",
        "It's okay."
    ]
}
```

Response:
```json
{
    "results": [
        {
            "tweet": "I love this product!",
            "score": 0.85
        },
        {
            "tweet": "This is terrible.",
            "score": -0.92
        },
        {
            "tweet": "It's okay.",
            "score": 0.12
        }
    ]
}
```

## ML Functioning

### Data Preparation
- Text cleaning (lowercase, special characters removal)
- TF-IDF vectorization with n-grams (1-3)
- Custom stopwords

### Model
- LogisticRegression with GridSearchCV
- Optimized parameters:
  - C: [0.1, 1.0, 10.0]
  - class_weight: ['balanced', None]
  - solver: ['lbfgs', 'liblinear']
  - max_iter: 1000

### Training
- Weekly execution (Sunday at 1:00 AM)
- Cross-validation (5 folds)
- Metrics: F1-score

## Maintenance

### Logs
- API: Docker console logs
- ML: `/var/log/cron.log`
- Database: MySQL logs

### Backup
- ML Models: stored in MinIO
- Database: standard MySQL backup

## Development

### Adding New Data
1. Add tweets to `db/sample-data.sql`
2. Rebuild database:
```bash
docker compose down -v
docker compose up -d
```

### Modifying ML Model
1. Modify `ml/train.py`
2. Rebuild ML service:
```bash
docker compose build ml
docker compose up -d ml
```

## Project Structure Details

### API Components

- **routes/**: API endpoints and request handling
- **services/**: Business logic implementation
- **schemas/**: Request/response validation schemas
- **models/**: Database models and ORM
- **exceptions/**: Custom exception classes
- **config/**: Configuration management
- **utils/**: Helper functions and utilities

### ML Components

- **train.py**: Main training script
- **utils/**: Helper functions for data processing

## Contribution

1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 