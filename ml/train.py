import re
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from utils.db import DatabaseOperations
from utils.s3 import upload_to_minio

db = DatabaseOperations()

# Get ALL data
last_data = db.fetch_last_7_days_data()
print(f"Total data retrieved: {len(last_data)}")

# Prepare data
data = {
    "text": [],
    "label": []
}

for element in last_data:
    data["text"].append(element["text"])
    # Use positive flag for binary classification
    data["label"].append(element["positive"])

df = pd.DataFrame(data)

def clean_text(text: str) -> str:
    """Enhanced text cleaning"""
    text = text.lower()
    # Keep some punctuation that might be important for sentiment
    text = re.sub(r'[^a-z\s!?.,]', '', text)
    # Replace multiple punctuation with single
    text = re.sub(r'([!?])\1+', r'\1', text)
    text = ' '.join(text.split())
    return text

df["text_clean"] = df["text"].apply(clean_text)

# Enhanced stopwords - keep sentiment-related words
english_stopwords = [
    "the", "and", "is", "in", "to", "of", "that", "was", "for",
    "on", "it", "this", "have", "has", "had", "with", "you", "they",
    "at", "be", "use", "your", "we", "can", "will", "or", "my", "than",
    "then", "else", "what", "when", "who", "which", "there", "from"
]

# Use TF-IDF with optimized parameters
vectorizer = TfidfVectorizer(
    stop_words=english_stopwords,
    max_features=300,  # Increased features
    ngram_range=(1, 3),  # Add trigrams
    min_df=2,
    max_df=0.95
)

X = vectorizer.fit_transform(df["text_clean"])
y = df["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define parameter grid for GridSearchCV
param_grid = {
    'C': [0.1, 1.0, 10.0],  # Regularization parameter
    'class_weight': ['balanced', None],
    'solver': ['lbfgs', 'liblinear'],
    'max_iter': [1000]
}

# Perform grid search with cross-validation
print("Performing grid search...")
grid_search = GridSearchCV(
    LogisticRegression(),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

# Print best parameters
print("\nBest parameters found:")
print(grid_search.best_params_)

# Use best model
model = grid_search.best_estimator_

# Evaluate on test set
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance analysis
feature_names = vectorizer.get_feature_names_out()
coefficients = model.coef_[0]
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': abs(coefficients)
})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\nTop 20 most important features:")
print(feature_importance.head(20))

# Test on example sentences
test_sentences = [
    "dirty son of a bitch",
    "you are pretty",
    "I don't know",
    "I love this product! It works great.",
    "Waste of resources and effort.",
    "Extremely poor quality.",
    "Save your money and look elsewhere.",
    "Nothing works as advertised."
]

print("\nTesting example sentences:")
test_clean = [clean_text(text) for text in test_sentences]
test_vectorized = vectorizer.transform(test_clean)
test_pred = model.predict(test_vectorized)
test_proba = model.predict_proba(test_vectorized)

for sentence, pred, proba in zip(test_sentences, test_pred, test_proba):
    sentiment = "Positive" if pred == 1 else "Negative"
    confidence = proba.max()
    print(f"\nText: {sentence}")
    print(f"Prediction: {sentiment} (confidence: {confidence:.2f})")
    print(f"Probabilities: Negative: {proba[0]:.2f}, Positive: {proba[1]:.2f}")

# Save models
file_model_name = 'trained_model.joblib'
joblib.dump(model, file_model_name)
print(f"\nModel saved to {file_model_name}")

file_vectorizer_name = 'vectorizer.joblib'
joblib.dump(vectorizer, file_vectorizer_name)
print(f"Vectorizer saved to {file_vectorizer_name}")

# Upload to MinIO
if upload_to_minio(file_model_name, 'ml-models', file_model_name):
    print("Model uploaded to MinIO successfully")
if upload_to_minio(file_vectorizer_name, 'ml-models', file_vectorizer_name):
    print("Vectorizer uploaded to MinIO successfully")