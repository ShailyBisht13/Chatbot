import React, { useRef } from "react";
import { Icon, Logo } from "./homeicons";
import "./messagebubble.css";

const LANG_MAP = {
  en: "en-US",
  hi: "hi-IN",
  bn: "bn-IN",
  mr: "mr-IN",
};

export default function MessageBubble({ message, language }) {
  const isUser = message.from === "user";
  const synthRef = useRef(window.speechSynthesis);

  /* ---------- SAFETY CHECK ---------- */
  if (!message || typeof message.text !== "string") {
    return null;
  }

  /* ---------- SPEAK ---------- */
  const speakText = (text) => {
    if (message.audio_url) {
      // ✅ Use Server-Side TTS instead of browser synth
      const audio = new Audio(`http://localhost:5000${message.audio_url}`);
      audio.play().catch((err) => console.error("Audio play failed:", err));
      return;
    }

    // Fallback to browser synthesis if no audio_url (rare now)
    if (!synthRef.current) return;
    const synth = synthRef.current;
    const langCode = LANG_MAP[language] || "en-US";
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = langCode;
    synth.cancel();
    synth.speak(utterance);
  };

  /* ---------- STOP ---------- */
  const stopSpeech = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
    }
  };

  const showTts = !isUser && !message.audio_url;

  return (
    <div className={`bubble-row ${isUser ? "user-row" : "bot-row"}`}>
      {!isUser && (
        <span className="bot-avatar" aria-hidden="true">
          <Logo />
        </span>
      )}

      <div className={`bubble ${isUser ? "user" : "bot"}`}>
        {message.image_path && (
          <div className="attached-img-container">
            <img
              src={
                message.image_path.startsWith("http")
                  ? message.image_path
                  : `http://localhost:5000/${message.image_path.replace(/\\/g, "/")}`
              }
              alt="User upload"
              className="user-attached-img"
            />
          </div>
        )}
        <div className="bubble-text">{message.text}</div>

        {/* 🧘 Meditation Audio */}
        {message.audio_url && (
          <div className="meditation-player">
            <audio controls autoPlay src={`http://localhost:5000${message.audio_url}`}>
              Your browser does not support the audio element.
            </audio>
          </div>
        )}

        {(showTts || message.time) && (
          <div className="bubble-foot">
            {/* 🔊 TTS controls (bot only) */}
            {showTts && (
              <div className="tts-controls">
                <button
                  type="button"
                  className="tts-btn"
                  onClick={() => speakText(message.text)}
                  title="Listen"
                  aria-label="Listen"
                >
                  {Icon.speaker(15)}
                </button>

                <button
                  type="button"
                  className="tts-btn stop"
                  onClick={stopSpeech}
                  title="Stop"
                  aria-label="Stop"
                >
                  {Icon.stop(15)}
                </button>
              </div>
            )}
            {message.time && <time className="bubble-time">{message.time}</time>}
          </div>
        )}
      </div>

      {isUser && (
        <span className="user-avatar" aria-hidden="true">
          {Icon.user(20)}
        </span>
      )}
    </div>
  );
}