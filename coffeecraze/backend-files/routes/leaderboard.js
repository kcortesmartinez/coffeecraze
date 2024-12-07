const express = require("express");
const Score = require("../models/Score");

const router = express.Router();

// Get leaderboard
router.get("/", async (req, res) => {
  try {
    const topScores = await Score.find().sort({ score: -1 }).limit(10).populate("userId", "username");
    res.json(topScores);
  } catch (err) {
    res.status(500).json({ error: "Error fetching leaderboard" });
  }
});

module.exports = router;