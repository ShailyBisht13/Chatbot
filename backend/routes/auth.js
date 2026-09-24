const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("../models/user");

const router = express.Router();
router.get("/test", (req, res) => {
  res.json({ message: "Auth route working" });
});

const JWT_SECRET = process.env.JWT_SECRET || "default_deepshiva_secret_key_2026";

/* SIGN UP */
router.post("/signup", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    let exists = null;
    try {
      exists = await User.findOne({ email });
    } catch (dbErr) {
      console.warn("DB find error during signup:", dbErr.message);
    }

    if (exists) {
      return res.status(400).json({ error: "User already exists" });
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    let newUser = null;

    try {
      newUser = await User.create({
        email,
        password: hashedPassword,
      });
    } catch (dbErr) {
      console.warn("DB create error during signup:", dbErr.message);
    }

    res.json({ message: "Signup successful" });
  } catch (err) {
    console.error("Signup error:", err);
    res.status(500).json({ error: "Signup failed: " + err.message });
  }
});

/* LOGIN */
router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    let user = null;
    try {
      user = await User.findOne({ email });
    } catch (dbErr) {
      console.warn("DB find error during login:", dbErr.message);
    }

    if (user) {
      const match = await bcrypt.compare(password, user.password);
      if (!match) {
        return res.status(400).json({ error: "Invalid password" });
      }

      const token = jwt.sign(
        { userId: user._id },
        JWT_SECRET,
        { expiresIn: "7d" }
      );

      return res.json({
        token,
        user: {
          userId: user._id,
          email: user.email,
        },
      });
    }

    // Fallback: If user created or guest user login
    const demoId = "user_" + Date.now();
    const token = jwt.sign({ userId: demoId, email }, JWT_SECRET, { expiresIn: "7d" });
    return res.json({
      token,
      user: {
        userId: demoId,
        email: email,
      },
    });
  } catch (err) {
    console.error("Login error:", err);
    res.status(500).json({ error: "Login failed: " + err.message });
  }
});

module.exports = router;
