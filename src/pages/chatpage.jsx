import React, { useEffect, useState } from "react";
import Sidebar from "../components/sidebar";
import ChatInput from "../components/chatinput";
import MessageBubble from "../components/messagebubble";
import "./chatpage.css";

export default function ChatPage() {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);

  useEffect(() => {
    const data = JSON.parse(localStorage.getItem("ds_convos") || "[]");
    setConversations(data);
    if (data.length) setActiveId(data[0].id);
  }, []);

  useEffect(() => {
    localStorage.setItem("ds_convos", JSON.stringify(conversations));
  }, [conversations]);

  const createNewChat = () => {
    const id = Date.now().toString();
    const chat = {
      id,
      title: 'Chat ${conversations.length + 1}',
      messages: [{ from: "bot", text: "🙏 Namaste, I am DeepShiva." }],
    };
    setConversations((p) => [chat, ...p]);
    setActiveId(id);
  };

  const updateMessages = (msgs) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === activeId ? { ...c, messages: msgs } : c))
    );
  };

  const sendToBackend = async (text) => {
    if (!activeId) createNewChat();

    const active = conversations.find((c) => c.id === activeId);
    const newMsgs = [...(active?.messages || []), { from: "user", text }];
    updateMessages(newMsgs);

    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, lang: "en" }),
      });
      const data = await res.json();
      updateMessages([...newMsgs, { from: "bot", text: data.reply }]);
    } catch {
      updateMessages([...newMsgs, { from: "bot", text: "Error connecting server" }]);
    }
  };

  const activeConversation = conversations.find((c) => c.id === activeId);

  return (
    <div className="ds-layout">
      <Sidebar
        conversations={conversations}
        onSelectConversation={setActiveId}
        onNewChat={createNewChat}
      />

      <div className="ds-chat">
        <div className="ds-chat-header">
          <div>
            <h2>DeepShiva Chat</h2>
            <p>Spiritual tourism assistant</p>
          </div>

          <select className="lang-select">
            <option value="en">English</option>
            <option value="hi">Hindi</option>
          </select>
        </div>

        <div className="ds-chat-messages">
          {(activeConversation?.messages || []).map((m, i) => (
            <MessageBubble key={i} message={m} />
          ))}
        </div>

        <ChatInput onSend={sendToBackend} />
      </div>
    </div>
  );
}
