import React, { useEffect, useState } from "react";
import Sidebar from "../components/sidebar";
import ChatInput from "../components/chatinput";
import MessageBubble from "../components/messagebubble";
import "./chatpage.css";

export default function ChatPage() {
  // conversations format: { id, title, preview, messages: [{from,text}], createdAt }
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);

  // load history from localStorage on mount
  useEffect(() => {
    try {
      const data = JSON.parse(localStorage.getItem("ds_convos") || "[]");
      setConversations(data);
      if (data.length) setActiveId(data[0].id);
    } catch (e) {
      console.warn("Failed to load conversations", e);
    }
  }, []);

  // persist whenever conversations change
  useEffect(() => {
    localStorage.setItem("ds_convos", JSON.stringify(conversations));
  }, [conversations]);

  const createNewChat = () => {
    const id = Date.now().toString();
    const c = {
      id,
      title: `Chat ${conversations.length + 1}`,
      preview: "",
      messages: [{ from: "bot", text: "🙏 Namaste, I am DeepShiva." }],
      createdAt: new Date().toISOString(),
    };
    setConversations((p) => [c, ...p]);
    setActiveId(id);
  };

  const updateActiveMessages = (newMessages) => {
    setConversations((prev) =>
      prev.map((c) =>
        c.id === activeId ? { ...c, messages: newMessages, preview: newMessages.slice(-1)[0]?.text || "" } : c
      )
    );
  };

  // send message (wraps your sendToBackend)
  const sendToBackend = async (userText) => {
    if (!activeId) createNewChat();
    // add user message locally
    let active = conversations.find((c) => c.id === activeId);
    if (!active) {
      createNewChat();
      active = conversations[0];
    }

    const newMessages = [...(active.messages || []), { from: "user", text: userText }];
    updateActiveMessages(newMessages);

    // send to server
    try {
      const res = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText, lang: "en" }), // replace with selected language
      });
      const data = await res.json();
      const botText = data.reply || "No reply";

      const afterBot = [...newMessages, { from: "bot", text: botText }];
      updateActiveMessages(afterBot);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectConversation = (id) => setActiveId(id);
  const handleDeleteConversation = (id) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) setActiveId(null);
  };

  // file attach handler (preview and later send)
  const handleFile = (file) => {
    if (!file) return;
    const url = URL.createObjectURL(file);
    // add as a user message containing media (preview)
    const active = conversations.find((c) => c.id === activeId);
    const newMessages = [...(active.messages || []), { from: "user", text: `[file:${file.name}]`, file: { name: file.name, url } }];
    updateActiveMessages(newMessages);

    // -> later upload file to backend using FormData
    // const fd = new FormData();
    // fd.append('file', file);
    // fetch('/upload', { method: 'POST', body: fd });
  };

  const activeConversation = conversations.find((c) => c.id === activeId);

  return (
    <div className="ds-page-layout">
      <Sidebar
        conversations={conversations}
        onSelectConversation={handleSelectConversation}
        onNewChat={createNewChat}
        onDeleteConversation={handleDeleteConversation}
      />

      <div className="ds-chat-area">
        <div className="ds-chat-header">
          <h3>{activeConversation?.title || "Start a new chat"}</h3>
        </div>

        <div className="ds-chat-messages">
          {(activeConversation?.messages || []).map((m, i) => (
            <MessageBubble key={i} message={m} />
          ))}
        </div>

        <div className="ds-chat-input">
          <ChatInput onSend={sendToBackend} onFile={handleFile} />
        </div>
      </div>
    </div>
  );
}
