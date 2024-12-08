const express = require("express");
const cors = require("cors");
const mongoose = require("mongoose");
require("dotenv").config();

const authRoutes = require("./routes/auth");
const gameRoutes = require("./routes/game");
const leaderboardRoutes = require("./routes/leaderboard");

const logger = require("./utils/logger");
app.use(logger);


// Will initialize the express app 
const app = express();
app.use(cors());
app.use(express.json());
app.use(logger); 

// Connects to the database
mongoose.connect(process.env.MONGO_URI, {useNewUrlParser: true, useUnifiedTopology: true})
    .then(() => console.log("Connected to MongoDB"))
    .catch((err) => console.error("Database connection error:", err));

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/game", gameRoutes);
app.use("/api/leaderboard", leaderboardRoutes);

// Starts server
const PORT = process.env.PORT || 5000; 
app.listen(PORT, () => console.log('Server running on port ${PORT}'))

// Bug Fixer 
console.log('Auth routes loaded');
console.log('Signup route triggered');