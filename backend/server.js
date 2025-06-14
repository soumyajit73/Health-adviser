const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(express.json());

// Routes
const calorieRoutes = require("./routes/calorieRoutes");
app.use("/api/calories", calorieRoutes);

app.get ("/", (req, res) => {
  res.send("Welcome to the Calorie Estimation API!");
});
const PORT = process.env.PORT || 5000;
app.listen  (PORT, () => {
  console.log(`Server is running on port http://localhost:${PORT}`);
});
