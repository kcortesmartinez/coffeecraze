const morgan = require("morgan");

const logger = morgan("dev"); // Logs HTTP requests in development mode

module.exports = logger;
