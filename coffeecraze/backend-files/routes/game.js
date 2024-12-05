const express = require("express");
const Score = require("../models/Score");

const router = express.Router();

// Submit game score
router.post("/submit", async (req, res) => {
  const { userId, score } = req.body;

  try {
    const newScore = new Score({ userId, score });
    await newScore.save();
    res.status(201).json({ message: "Score submitted successfully" });
  } catch (err) {
    res.status(500).json({ error: "Error submitting score" });
  }
});

module.exports = router;