import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample training data (you can use real data later)
data = {
    'age': [21, 25, 30, 35, 40, 20, 28, 32, 19, 45],
    'gender': [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    'height': [170, 160, 175, 165, 180, 158, 168, 155, 162, 178],
    'weight': [67, 55, 75, 60, 85, 58, 72, 52, 50, 90],
    'activity': [1.2, 1.55, 1.375, 1.2, 1.725, 1.2, 1.55, 1.375, 1.2, 1.9],
    'calories': [2000, 1800, 2500, 1900, 2800, 1700, 2400, 1600, 1500, 3000]
}


df = pd.DataFrame(data)

# Features and target
X = df[['age', 'gender', 'height', 'weight', 'activity']]
y = df['calories']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'calorie_predictor.pkl')
print("Model trained and saved.")
