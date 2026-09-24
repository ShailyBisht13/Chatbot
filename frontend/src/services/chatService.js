// src/services/chatService.js
import axios from "axios";

const API_URL = "http://localhost:5000/api/chat";

export async function sendMessage(query, language = "en", imagePath = null) {
  try {
    const token = localStorage.getItem("token"); // optional (for later)

    const response = await axios.post(
      API_URL,
      {
        query,
        language,
        imagePath, // ✅ Pass image path
        persona:
          language === "hi"
            ? "hindi"
            : language === "bn"
              ? "bengali"
              : language === "mr"
                ? "marathi"
                : "english",

      },
      {
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      }
    );

    return response.data; // { reply: "..." }
  } catch (error) {
    console.error("Chat API error:", error);
    throw new Error("Chat server unavailable");
  }
}
