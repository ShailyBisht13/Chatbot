import React, { useState, useRef } from "react";
import { Icon } from "./homeicons";
import "./chatinput.css";
import QRScanner from "./qrscanner";

/* QR camera icon (the other icons come from homeicons) */
const CameraIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
    <circle cx="12" cy="13" r="4" />
  </svg>
);

export default function ChatInput({ onSend, placeholder, language, onImageUpload, attachedImage, onClearImage }) {
  const [text, setText] = useState("");
  const [showQR, setShowQR] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const recognitionRef = useRef(null);

  /* ---------- SEND MESSAGE ---------- */
  const send = () => {
    // Allow sending if text OR attached image exists
    if (!text.trim() && !attachedImage) return;
    onSend(text);
    setText("");
  };

  /* ---------- FILE UPLOAD ---------- */
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setUploadSuccess(false);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();

      if (onImageUpload) {
        onImageUpload(data.filePath);
      }
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 3000);
    } catch (err) {
      alert("Upload failed: " + err.message);
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  /* ---------- VOICE INPUT ---------- */
  const handleMic = () => {
    // If currently listening, stop it
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;

      recognition.lang =
        language === "hi"
          ? "hi-IN"
          : language === "bn"
            ? "bn-IN"
            : language === "mr"
              ? "mr-IN"
              : "en-US";

      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setText((prev) => (prev ? `${prev} ${transcript}` : transcript));
        }
        setIsListening(false);
      };

      recognition.onerror = (err) => {
        console.error("Speech recognition error:", err);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (err) {
      console.error("Failed to start mic:", err);
      setIsListening(false);
    }
  };

  return (
    <>
      {showQR && (
        <QRScanner
          onScan={(data) => {
            if (!data) return;
            if (data.startsWith("http://") || data.startsWith("https://")) {
              window.open(data, "_blank");
            } else {
              setText(data);
            }
            setShowQR(false);
          }}
          onClose={() => setShowQR(false)}
        />
      )}

      <div className="chat-composer">
        {/* Attached image chip */}
        {attachedImage && (
          <div className="attached-preview-bar" role="status">
            <span className="attached-icon">{Icon.image(16)}</span>
            <span className="attached-name">
              Photo attached: {attachedImage.split(/[\\/]/).pop()}
            </span>
            <button
              type="button"
              className="remove-img-btn"
              onClick={onClearImage}
              title="Remove image"
              aria-label="Remove image"
            >
              {Icon.close(14)}
            </button>
          </div>
        )}

        {/* Listening status */}
        {isListening && (
          <div className="listening-indicator-bar" role="status" aria-live="polite">
            <span className="pulse-dot" />
            <span>Listening... Speak now</span>
            <span className="wave" aria-hidden="true">
              <i /><i /><i /><i /><i />
            </span>
          </div>
        )}

        <div className="chat-input-row">
          {/* Input pill: attach · text · QR · mic */}
          <div className={`chat-input-bar ${isListening ? "is-listening" : ""}`}>
            <label
              className={`icon-btn ${isUploading ? "is-busy" : ""} ${uploadSuccess ? "is-success" : ""}`}
              title="Attach Image"
            >
              {isUploading ? <span className="spinner" /> : uploadSuccess ? Icon.check(22) : Icon.image(22)}
              <input
                type="file"
                accept="image/*"
                hidden
                onChange={handleFileChange}
                disabled={isUploading}
              />
            </label>

            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={isListening ? "Listening..." : placeholder}
              onKeyDown={(e) => e.key === "Enter" && send()}
              aria-label="Message"
            />

            <button
              type="button"
              className="icon-btn"
              onClick={() => setShowQR(true)}
              title="Scan QR"
              aria-label="Scan QR"
            >
              <CameraIcon />
            </button>

            <button
              type="button"
              className={`icon-btn ${isListening ? "listening-btn" : ""}`}
              onClick={handleMic}
              title={isListening ? "Stop Listening" : "Speak with Mic"}
              aria-label={isListening ? "Stop Listening" : "Speak with Mic"}
            >
              {isListening ? Icon.stop(20) : Icon.mic(20)}
            </button>
          </div>

          <button type="button" className="send-btn" onClick={send} aria-label="Send message">
            {Icon.send(24)}
          </button>
        </div>
      </div>
    </>
  );
}