// testMongo.js — checks MongoDB connection + a write, then cleans up.
// Run from the main folder: node testMongo.js
const path = require("path");

// Use the packages installed in backend/node_modules
const backendDir = path.join(__dirname, "backend");
const load = (name) => require(require.resolve(name, { paths: [backendDir] }));

const mongoose = load("mongoose");
load("dotenv").config({ path: path.join(backendDir, ".env") });

// Same database the app uses
const uri = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/projectds";

mongoose
  .connect(uri, { serverSelectionTimeoutMS: 5000 })
  .then(async () => {
    console.log(`✅ Mongo connected (db: ${mongoose.connection.name})`);

    const Test = mongoose.model("ConnectionTest", new mongoose.Schema({ name: String }));
    await Test.create({ name: "test-ok" });
    console.log("✅ Write successful");

    await Test.collection.drop().catch(() => {}); // don't leave junk behind
    await mongoose.disconnect();
    process.exit(0);
  })
  .catch((err) => {
    console.error("❌ Mongo write failed:", err.message);
    process.exit(1);
  });
