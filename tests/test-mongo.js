// test-mongo.js — checks that MONGO_URI from backend/.env connects.
// Run from the main folder: node test-mongo.js
const path = require("path");

// Use the packages installed in backend/node_modules
const backendDir = path.join(__dirname, "backend");
const load = (name) => require(require.resolve(name, { paths: [backendDir] }));

const mongoose = load("mongoose");
load("dotenv").config({ path: path.join(backendDir, ".env") });

const uri = process.env.MONGO_URI;
if (!uri) {
  console.error("❌ MONGO_URI is not set in backend/.env");
  process.exit(1);
}

mongoose
  .connect(uri, { serverSelectionTimeoutMS: 5000 })
  .then(async () => {
    console.log(`✅ Connected to MongoDB (db: ${mongoose.connection.name})`);
    await mongoose.disconnect();
    process.exit(0);
  })
  .catch((err) => {
    console.error("❌ Connection failed ->", err.message || err);
    process.exit(1);
  });