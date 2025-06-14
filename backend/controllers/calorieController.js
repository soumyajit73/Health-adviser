const axios = require('axios');

exports.getCalorieEstimate = async (req, res) => {
  const { age, gender, height, weight, activityLevel } = req.body;

  if (!age || !gender || !height || !weight || !activityLevel) {
    return res.status(400).json({ error: 'All fields are required' });
  }

  try {
    const response = await axios.post('http://127.0.0.1:5001/predict', {
      age,
      gender,
      height,
      weight,
      activityLevel
    });

    const predictedCalories = response.data.predictedCalories;

    return res.status(200).json({
      predictedCalories
    });

  } catch (error) {
    console.error("ML API Error:", error.message);
    return res.status(500).json({ error: 'Something went wrong with the ML model' });
  }
};
