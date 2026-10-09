// test-mongo.js
require("dotenv").config();
const mongoose = require("mongoose");

mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    console.log("✅ Test: connected to MongoDB Atlas");
    process.exit(0);
  })
  .catch(err => {
    console.error("❌ Test: connection failed ->", err.message || err);
    process.exit(1);
  });