import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
data = pd.read_csv("spam.csv")

# Features & labels
X_text = data["message"]
y = data["label"]

# Convert text to numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_text)

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model & vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved successfully")
