import re
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from utils.db import DatabaseOperations
from utils.s3 import upload_to_minio

db = DatabaseOperations()

# Get ALL data
last_data = db.fetch_all_training_data()
print(f"Total data retrieved: {len(last_data)}")

# Prepare data with better labeling
data = {
    "text": [],
    "label": []
}

for element in last_data:
    data["text"].append(element["text"])
    # Consider both positive and negative flags
    if element["positive"] == 1:
        data["label"].append(1)  # Positive
    elif element["negative"] == 1:
        data["label"].append(0)  # Negative
    else:
        data["label"].append(2)  # Neutral

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

# Use TF-IDF with better parameters
vectorizer = TfidfVectorizer(
    stop_words=english_stopwords,
    max_features=500,  # Increased features
    ngram_range=(1, 3),  # Add trigrams
    min_df=2,
    max_df=0.95  # Remove very common words
)

X = vectorizer.fit_transform(df["text_clean"])
y = df["label"]

# Use RandomForest instead of LogisticRegression
model = RandomForestClassifier(
    n_estimators=200,  # More trees
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight='balanced',
    random_state=42
)

# Final training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance analysis
feature_names = vectorizer.get_feature_names_out()
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
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
    sentiment = "Positive" if pred == 1 else "Negative" if pred == 0 else "Neutral"
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