const Joi = require("joi");

const validateScore = (data) => {
  const schema = Joi.object({
    userId: Joi.string().required(),
    score: Joi.number().min(0).required(),
  });
  return schema.validate(data);
};

module.exports = validateScore;
