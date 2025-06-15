document.getElementById("calorieForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const data = {
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    height: document.getElementById("height").value,
    weight: document.getElementById("weight").value,
    duration: document.getElementById("duration").value,
    heart_rate: document.getElementById("heart_rate").value,
    body_temp: document.getElementById("body_temp").value,
    activity_level: document.getElementById("activity_level").value,
  };

  const res = await fetch("http://localhost:5001/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const result = await res.json();

  if (res.ok) {
    document.getElementById("result").style.display = "block";
    document.getElementById("burned").innerText = `🔥 Calories Burned: ${result.caloriesBurned} kcal`;
    document.getElementById("maintenance").innerText = `🍽️ Maintenance Calories (TDEE): ${result.maintenanceCalories} kcal`;
    window.currentTDEE = result.maintenanceCalories;
    window.caloriesBurned = result.caloriesBurned;
    window.currentWeight = data.weight;
  } else {
    alert(result.error || "Prediction failed.");
  }
});

function calculateDeficit() {
  const targetWeight = document.getElementById("targetWeight").value;
  const currentWeight = parseFloat(window.currentWeight);
  const tdee = parseFloat(window.currentTDEE);
  const burned = parseFloat(window.caloriesBurned);

  if (!targetWeight || isNaN(targetWeight)) {
    document.getElementById("suggestion").innerText = "⚠️ Please enter a valid target weight.";
    return;
  }

  const weightDiff = currentWeight - targetWeight;
  const totalCalorieChange = weightDiff * 7700; // 1kg ≈ 7700 kcal
  const daysEstimate = Math.ceil(Math.abs(totalCalorieChange) / 500); // assuming 500 kcal/day change

  let suggestionText = "";

  if (weightDiff > 0) {
    const dailyDeficit = (totalCalorieChange / daysEstimate).toFixed(0);
    suggestionText = `To lose ${weightDiff} kg, aim for a daily deficit of ~${dailyDeficit} kcal. Estimated time: ${daysEstimate} days.`;
  } else if (weightDiff < 0) {
    const dailySurplus = (Math.abs(totalCalorieChange) / daysEstimate).toFixed(0);
    suggestionText = `To gain ${Math.abs(weightDiff)} kg, aim for a daily surplus of ~${dailySurplus} kcal. Estimated time: ${daysEstimate} days.`;
  } else {
    suggestionText = "🎉 You are already at your target weight!";
  }

  document.getElementById("suggestion").innerText = suggestionText;
}
