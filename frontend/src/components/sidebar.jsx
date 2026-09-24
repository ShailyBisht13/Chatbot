import React from "react";
import { Logo } from "./homeicons";
import "./sidebar.css";

const Svg = ({ children, size = 16 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.9"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    {children}
  </svg>
);

const PlusIcon = () => (
  <Svg size={17}>
    <path d="M12 5v14M5 12h14" />
  </Svg>
);
const ChatIcon = () => (
  <Svg>
    <path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" />
  </Svg>
);
const TrashIcon = () => (
  <Svg size={15}>
    <path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14M10 11v5M14 11v5" />
  </Svg>
);

export default function Sidebar({
  conversations,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  language,
  text,
  activeId, // optional: highlights the open chat
}) {
  return (
    <aside className="ds-sidebar">
      {/* Header */}
      <div className="ds-sidebar-header">
        <div className="ds-brand">
          <span className="ds-brand-mark" aria-hidden="true"><Logo /></span>
          <h3>{text.appName}</h3>
        </div>

        <button className="new-chat-btn" onClick={onNewChat}>
          <PlusIcon />
          <span>{text.newChat.replace(/^\+\s*/, "")}</span>
        </button>
      </div>

      {/* Chat list */}
      <nav className="ds-chat-list" aria-label={text.chat}>
        {conversations.map((c, index) => (
          <div
            key={c.id}
            className={`ds-chat-item ${c.id === activeId ? "active" : ""}`}
          >
            <button
              type="button"
              className="chat-select"
              onClick={() => onSelectConversation(c.id)}
              aria-current={c.id === activeId ? "true" : undefined}
            >
              <ChatIcon />
              <span className="chat-title">
                {text.chat} {conversations.length - index}
              </span>
            </button>

            {/* Delete button */}
            <button
              type="button"
              className="delete-chat"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteConversation(c.id);
              }}
              title="Delete chat"
              aria-label="Delete chat"
            >
              <TrashIcon />
            </button>
          </div>
        ))}
      </nav>
    </aside>
  );
}