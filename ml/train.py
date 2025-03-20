import re

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from db import DatabaseOperations

db = DatabaseOperations()

# Get data from database
last_data = db.fetch_last_7_days_data()

data = {
    "text": [],
    "label": []
}

for element in last_data:
    data["text"].append(element["text"])
    data["label"].append(element["positive"])

print(data)
df = pd.DataFrame(data)

def clean_text(text: str) -> str:
    text = text.lower()  # Mettre en minuscule
    text = re.sub(r"[^\w\s]", "", text)  # Supprimer les caractères spéciaux

    return text


df["text_clean"] = df["text"].apply(clean_text)

french_stopwords = [
    "le",
    "la",
    "les",
    "un",
    "une",
    "des",
    "du",
    "de",
    "dans",
    "et",
    "en",
    "au",
    "aux",
    "avec",
    "ce",
    "ces",
    "pour",
    "par",
    "sur",
    "pas",
    "plus",
    "où",
    "mais",
    "ou",
    "donc",
    "ni",
    "car",
    "ne",
    "que",
    "qui",
    "quoi",
    "quand",
    "à",
    "son",
    "sa",
    "ses",
    "ils",
    "elles",
    "nous",
    "vous",
    "est",
    "sont",
    "cette",
    "cet",
    "aussi",
    "être",
    "avoir",
    "faire",
    "comme",
    "tout",
    "bien",
    "mal",
    "on",
    "lui",
]

# Vectorisation (bag of words)
vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
X = vectorizer.fit_transform(df["text_clean"])
y = df["label"]

# Division des données
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Entraînement du modèle
model = LogisticRegression()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred))

# Matrice de confusion
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# Nouvelles données
new_comments = [
    "Je ne supporte pas cette personne.",  # Haineux
    "Cette vidéo est incroyable, merci pour votre travail.",  # Non haineux
    "Arrête de dire n'importe quoi, imbécile.",  # Haineux
    "Une excellente présentation, bravo à toute l'équipe.",  # Non haineux
]

# Nettoyage et vectorisation
new_comments_clean = [clean_text(comment) for comment in new_comments]
new_comments_vectorized = vectorizer.transform(new_comments_clean)

# Prédictions
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Haineux' if label == 1 else 'Non haineux'}")
