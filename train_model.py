import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

print("--- Loading Market Data ---")
df = pd.read_csv('market_data.csv')
df['Future_MidPrice'] = df['MidPrice'].shift(-5) 
df['Price_Change'] = abs(df['Future_MidPrice'] - df['MidPrice'])
df['Target'] = (df['Price_Change'] > 0.20).astype(int)

df = df.dropna()

print(f"Data Prepared: {len(df)} rows")
print(f"Toxic Events (High Volatility): {df['Target'].sum()} instances")


features = ['Spread', 'Imbalance', 'BestBid', 'BestAsk']
X = df[features]
y = df['Target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("\n--- Training Random Forest Classifier ---")
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)


print("\n--- Model Evaluation ---")
predictions = model.predict(X_test)


print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

importances = model.feature_importances_
print("\n--- What Drives the Market? ---")
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance:.4f}")