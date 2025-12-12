import React from "react";
import "./messagebubble.css";

function MessageBubble({ message }) {
  const isUser = message.from === "user";

  return (
    <div className={`bubble-row ${isUser ? "user-row" : "bot-row"}`}>
      <div className={`bubble ${isUser ? "user" : "bot"}`}>{message.text}</div>
    </div>
  );
}

export default MessageBubble;
