import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset
df = pd.read_csv("phishing_site_urls/phishing_site_urls.csv")

# Check the first few rows of the dataset to confirm the column names
print(df.head())

# Ensure the column names are correct (case-sensitive)
df['Label'] = df['Label'].map({'bad': 1, 'good': 0})

# Feature extraction
df['url_length'] = df['URL'].apply(lambda x: len(x))  # Use the correct column name 'URL'
df['has_https'] = df['URL'].apply(lambda x: int('https' in x))  # Use 'URL' instead of 'url'
df['has_login'] = df['URL'].apply(lambda x: int('login' in x))
df['has_verify'] = df['URL'].apply(lambda x: int('verify' in x))
df['has_update'] = df['URL'].apply(lambda x: int('update' in x))

# Features and target
X = df[['url_length', 'has_https', 'has_login', 'has_verify', 'has_update']]
y = df['Label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "phishing_model.pkl")

# Confirm model training completion
print("✅ Model training complete. 'phishing_model.pkl' saved.")
