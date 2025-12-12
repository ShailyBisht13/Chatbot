import React, { useRef } from "react";
import "./chatinput.css";

/**
 * Props:
 *  - onSend(text)        => called when user presses OM or Enter
 *  - onVoiceInput()      => called when mic pressed
 *  - onFile(file)        => called when a file is selected via +
 */
export default function ChatInput({ onSend, onVoiceInput, onFile }) {
  const textRef = useRef(null);
  const fileRef = useRef(null);

  const handleSend = () => {
    const val = textRef.current.value.trim();
    if (!val) return;
    onSend && onSend(val);
    textRef.current.value = "";
  };

  const handleFileChange = (e) => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    onFile && onFile(f);
    e.target.value = null;
  };

  return (
    <div className="ds-chatinput-wrapper">
      {/* plus button */}
      <button
        className="ds-plus-btn"
        title="Attach file"
        onClick={() => fileRef.current && fileRef.current.click()}
      >
        ＋
      </button>

      <input
        ref={fileRef}
        type="file"
        accept="image/*,video/*,audio/*"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />

      {/* input box with icons to the right */}
      <div className="ds-input-box">
        <input
          ref={textRef}
          className="ds-text-input"
          placeholder="Ask DeepShiva..."
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <div className="ds-input-icons">
          {/* mic icon */}
          <button
            className="ds-icon-btn"
            title="Voice input"
            onClick={() => onVoiceInput && onVoiceInput()}
          >
            <img
              src="https://i.imgur.com/0T1R3xk.png"
              alt="mic"
              className="ds-icon-img"
            />
          </button>

          {/* OM send icon */}
          <button
            className="ds-send-btn"
            title="Send"
            onClick={handleSend}
          >
            <img
              src="https://i.imgur.com/x0jvC7d.png"
              alt="om"
              className="ds-om-img"
            />
          </button>
        </div>
      </div>
    </div>
  );
}
