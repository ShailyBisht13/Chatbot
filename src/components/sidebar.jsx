import React, { useState, useEffect } from "react";
import "./sidebar.css";

export default function Sidebar({
  conversations,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
}) {
  const [open, setOpen] = useState(true);

  return (
    <div className={`ds-sidebar ${open ? "open" : "closed"}`}>
      <div className="ds-sidebar-top">
        <button
          className="ds-hamburger"
          onClick={() => setOpen((s) => !s)}
          aria-label="toggle menu"
        >
          ☰
        </button>

        {open && (
          <>
            <h3 className="ds-title">DeepShiva</h3>
            <button className="ds-new" onClick={onNewChat}>＋ New Chat</button>
          </>
        )}
      </div>

      {open && (
        <div className="ds-history">
          {conversations.length === 0 && (
            <div className="ds-empty">No conversations yet.</div>
          )}
          {conversations.map((c) => (
            <div key={c.id} className="ds-convo">
              <button
                className="ds-convo-btn"
                onClick={() => onSelectConversation(c.id)}
                title={c.preview}
              >
                <div className="ds-convo-title">{c.title || "Chat"}</div>
                <div className="ds-convo-preview">
                  {c.preview ? c.preview.slice(0, 60) : "—"}
                </div>
              </button>
              <button
                className="ds-delete"
                onClick={() => onDeleteConversation(c.id)}
                aria-label="delete conversation"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
