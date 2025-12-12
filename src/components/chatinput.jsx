import { useState } from "react";
import "./chatinput.css";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");

  const send = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="chat-input-bar">
      {/* LEFT + */}
      <button className="icon-btn left">＋</button>

      {/* INPUT */}
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ask anything about Shiva..."
        onKeyDown={(e) => e.key === "Enter" && send()}
      />

      {/* RIGHT ICONS */}
      <button className="icon-btn">🕉</button>
      <button className="icon-btn">🎤</button>
    </div>
  );
}
