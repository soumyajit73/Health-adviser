import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load dataset
df = pd.read_csv('calories.csv')
df['Gender'] = df['Gender'].map({'male': 1, 'female': 0})

# Features and target
X = df[['Gender', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']]
y = df['Calories']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ R² score:", r2_score(y_test, y_pred))
print("📉 MSE:", mean_squared_error(y_test, y_pred))
print("📊 MAE:", mean_absolute_error(y_test, y_pred))

# Save model
joblib.dump(model, 'calorie_predictor.pkl')
print("✅ Model trained and saved as calorie_predictor.pkl")
