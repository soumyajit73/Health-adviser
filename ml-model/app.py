from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend/backend

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
        age = int(data['age'])
        gender = data['gender']
        height = float(data['height'])
        weight = float(data['weight'])
        activity = data['activityLevel']

        # ✅ Dummy calorie prediction (replace with ML model later)
        base_calories = (10 * weight) + (6.25 * height) - (5 * age)
        if gender == 'male':
            base_calories += 5
        else:
            base_calories -= 161

        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very': 1.725,
            'extra': 1.9
        }

        multiplier = activity_multipliers.get(activity, 1.2)
        predicted = round(base_calories * multiplier)

        return jsonify({'predictedCalories': predicted})

    except Exception as e:
        print("🚨 Flask Error:", str(e))
        return jsonify({'error': 'Server error occurred'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
