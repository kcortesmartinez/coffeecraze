const jwt = require("jsonwebtoken");

const generateToken = (userId) => {
  try {
    return jwt.sign({ id: userId }, process.env.JWT_SECRET, { expiresIn: "1h" });
  } catch (error) {
    console.error("Error generating token:", error);
    return null;
  }
};

module.exports = generateToken;