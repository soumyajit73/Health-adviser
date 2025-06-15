from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load your trained model
model = joblib.load("calorie_predictor.pkl")

@app.route('/')
def home():
    return "Flask ML API is running."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("📦 Incoming data:", data)

    required_keys = ['age', 'gender', 'height', 'weight', 'activityLevel']
    if not all(key in data for key in required_keys):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Convert data to ML model input format
        age = int(data['age'])
        gender = 1 if data['gender'] == 'male' else 0
        height = float(data['height'])
        weight = float(data['weight'])

        activity_map = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very': 1.725,
            'extra': 1.9
        }
        activity = activity_map.get(data['activityLevel'], 1.2)

        # Make prediction
        input_df = pd.DataFrame([{
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'activity': activity
        }])

        prediction = model.predict(input_df)[0]
        predicted_calories = int(round(prediction))

        return jsonify({'predictedCalories': predicted_calories})

    except Exception as e:
        print("🚨 Prediction error:", str(e))
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
