// // server.js

// require("dotenv").config();        // Load .env first
// const express = require("express");
// const mongoose = require("mongoose");
// const cors = require("cors");

// // Routes
// const chatRoute = require("./routes/chat");

// const app = express();

// /* -------------------- MIDDLEWARE -------------------- */
// app.use(cors());
// app.use(express.json());

// /* -------------------- ROUTES -------------------- */
// app.use("/api", chatRoute);

// app.get("/", (req, res) => {
//   res.send("✅ Backend is running");
// });

// /* -------------------- MONGODB CONNECTION -------------------- */
// mongoose
//   .connect(process.env.MONGO_URI)
//   .then(() => {
//     console.log("✅ MongoDB connected");
//   })
//   .catch((err) => {
//     console.error("❌ MongoDB connection error:", err.message);
//   });

// /* -------------------- SERVER -------------------- */
// const PORT = process.env.PORT || 5000;

// app.listen(PORT, () => {
//   console.log(`🚀 Server running at http://localhost:${PORT}`);
// });


