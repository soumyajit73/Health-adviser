const express = require('express');
const router = express.Router();
const { getCalorieEstimate } = require('../controllers/calorieController');

router.post('/', getCalorieEstimate);

module.exports = router;
