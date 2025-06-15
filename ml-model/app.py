from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend/backend communication

# Load the trained model
model = joblib.load("calorie_predictor.pkl")

@app.route('/')
def home():
    return "Flask ML API is running with trained model."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("📦 Incoming data:", data)

    # Check required inputs
    required_keys = ['age', 'gender', 'height', 'weight', 'duration', 'heart_rate', 'body_temp']
    if not all(key in data for key in required_keys):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Convert gender to numeric
        gender = 1 if data['gender'].strip().lower() == 'male' else 0

        # Prepare input DataFrame
        input_df = pd.DataFrame([{
            'Gender': gender,
            'Age': int(data['age']),
            'Height': float(data['height']),
            'Weight': float(data['weight']),
            'Duration': float(data['duration']),
            'Heart_Rate': float(data['heart_rate']),
            'Body_Temp': float(data['body_temp'])
        }])

        # Make prediction
        prediction = model.predict(input_df)[0]
        predicted_calories = max(0, round(prediction, 2))  # Clamp negative values to 0

        return jsonify({'predictedCalories': predicted_calories})

    except Exception as e:
        print("🚨 Error:", e)
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
