document
  .getElementById("calorieForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const duration = document.getElementById("duration").value;
    const heart_rate = document.getElementById("heart_rate").value;
    const body_temp = document.getElementById("body_temp").value;

    const response = await fetch("http://localhost:5001/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
     body: JSON.stringify({
  age: parseInt(age),
  gender: gender.toLowerCase(),
  height: parseFloat(height),
  weight: parseFloat(weight),
  duration: parseFloat(duration),
  heart_rate: parseFloat(heart_rate),
  body_temp: parseFloat(body_temp),
}),

    });

    const resultDiv = document.getElementById("result");
    const data = await response.json();

    if (response.ok) {
      resultDiv.innerHTML = `<h3>🔥 Predicted Calorie Burn: ${data.predictedCalories} kcal</h3>`;
    } else {
      resultDiv.innerHTML = `<p style="color:red;">❌ Error: ${data.error}</p>`;
    }
  });
