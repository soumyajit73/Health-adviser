from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("calorie_predictor.pkl")

# Activity level factors for TDEE
activity_factors = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'very': 1.725,
    'extra': 1.9
}

@app.route('/')
def home():
    return "Flask ML API running."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("📦 Incoming data:", data)

    required_keys = ['age', 'gender', 'height', 'weight', 'duration', 'heart_rate', 'body_temp', 'activity_level']
    for key in required_keys:
        if key not in data or data[key] in [None, '']:
            return jsonify({'error': f'Missing or empty field: {key}'}), 400

    try:
        # Extract and convert inputs
        age = int(data['age'])
        gender = data['gender'].lower()
        height = float(data['height'])
        weight = float(data['weight'])
        duration = float(data['duration'])
        heart_rate = float(data['heart_rate'])
        body_temp = float(data['body_temp'])
        activity_level = data['activity_level'].lower()

        # Check valid activity level
        if activity_level not in activity_factors:
            return jsonify({'error': 'Invalid activity level'}), 400

        gender_numeric = 1 if gender == 'male' else 0

        # Construct input DataFrame for prediction
        input_df = pd.DataFrame([{
            'Gender': gender_numeric,
            'Age': age,
            'Height': height,
            'Weight': weight,
            'Duration': duration,
            'Heart_Rate': heart_rate,
            'Body_Temp': body_temp
        }])

        # Predict calories burned using model
        predicted_burn = round(model.predict(input_df)[0], 2)

        # Calculate BMR (Mifflin-St Jeor Equation)
        bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == 'male' else -161)

        # Calculate TDEE
        tdee = round(bmr * activity_factors[activity_level], 2)

        # Targets
        loss_target = round(tdee - 500, 2)
        gain_target = round(tdee + 500, 2)
        remaining_burn = max(0, 500 - predicted_burn)

        return jsonify({
            'caloriesBurned': predicted_burn,
            'maintenanceCalories': tdee,
            'weightLossTarget': loss_target,
            'weightGainTarget': gain_target,
            'suggestion': f"Burn {remaining_burn} more kcal or reduce intake by the same to hit fat-loss goal."
        })

    except Exception as e:
        print("🚨 Error:", e)
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
