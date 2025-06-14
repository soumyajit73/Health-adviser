document
  .getElementById("calorieForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const activityLevel = document.getElementById("activityLevel").value;

    if (!age || !gender || !height || !weight || !activityLevel) {
      alert("Please fill out all fields!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/calories", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          age,
          gender,
          height,
          weight,
          activityLevel,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        document.getElementById(
          "result"
        ).innerText = `Estimated Daily Calories: ${data.predictedCalories} kcal`;
      } else {
        document.getElementById("result").innerText = `Error: ${
          data.error || "Something went wrong"
        }`;
      }
    } catch (err) {
      document.getElementById("result").innerText = "Server error!";
      console.error("Fetch error:", err);
    }
  });
