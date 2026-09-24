const express = require("express");
const Chat = require("../models/chat");
const router = express.Router();
const auth = require("../middleware/auth");
// ✅ LOAD chats (FIRST)
// 🔥 1️⃣ LOAD chats — MUST BE FIRST
router.get("/load", auth, async (req, res) => {
  try {
    const chat = await Chat.findOne({ userId: req.user.userId });
    res.json(chat?.conversations || []);
  } catch (err) {
    console.error("Load chat error:", err);
    res.status(500).json({ error: "Failed to load chats" });
  }
});

// 🔥 2️⃣ SAVE chats
router.post("/save", auth, async (req, res) => {
  try {
    const { conversations } = req.body;
    console.log(`[DEBUG] Saving ${conversations?.length || 0} conversations for user: ${req.user.userId}`);

    const result = await Chat.findOneAndUpdate(
      { userId: req.user.userId },
      { conversations },
      { upsert: true, new: true }
    );

    console.log(`[DEBUG] Save success. Document ID: ${result._id}`);
    res.json({ success: true });
  } catch (err) {
    console.error("Save chat error:", err);
    res.status(500).json({ error: "Save failed" });
  }
});

// ❗ 3️⃣ DYNAMIC ROUTES — ALWAYS LAST
router.get("/:userId", async (req, res) => {
  // if you really need this
});

// ❌ KEEP DYNAMIC ROUTES LAST (if any)
// router.get("/:userId", ...)
module.exports = router;