const mongoose = require("mongoose");

const MessageSchema = new mongoose.Schema(
  {
    from: { type: String, enum: ["user", "bot"], required: true },
    text: { type: String, required: true },
  },
  { _id: false }
);

const ConversationSchema = new mongoose.Schema(
  {
    id: { type: String, required: true }, // using ID from frontend
    title: { type: String },
    messages: [MessageSchema],
  },
  { _id: false }
);

const ChatSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
      unique: true, // One doc per user
    },
    conversations: [ConversationSchema],
  },
  { timestamps: true }
);

module.exports = mongoose.models.Chat || mongoose.model("Chat", ChatSchema);