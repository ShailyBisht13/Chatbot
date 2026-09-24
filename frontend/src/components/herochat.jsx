import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { sendMessage } from "../services/chatService";
import { Icon, Logo } from "./homeicons";
import kedarnathImg from "../assets/kedarnath.jpg";
import "./herochat.css";

const API = "http://localhost:5000";

const LANG_MAP = { en: "en-US", hi: "hi-IN", bn: "bn-IN", mr: "mr-IN" };

/* text that depends on the selected language (same wording as the chat page) */
const TXT = {
  en: {
    placeholder: "Ask anything... (e.g. yatra, weather, routes, rituals)",
    typing: "Deepshiva is typing...",
    error: "Server error",
  },
  hi: {
    placeholder: "मंदिर, ध्यान, योग या आध्यात्मिक यात्रा के बारे में पूछें...",
    typing: "दीपशिवा लिख रहा है...",
    error: "सर्वर से कनेक्शन नहीं हो पाया",
  },
  bn: {
    placeholder: "মন্দির, ধ্যান, যোগ বা আধ্যাত্মিক যাত্রা সম্পর্কে জিজ্ঞাসা করুন...",
    typing: "দীপশিবা টাইপ করছে...",
    error: "সার্ভারের সাথে সংযোগ ব্যর্থ হয়েছে",
  },
  mr: {
    placeholder: "मंदिरे, ध्यान, योग किंवा आध्यात्मिक प्रवासाबद्दल विचारा...",
    typing: "दीपशिवा टाइप करत आहे...",
    error: "सर्व्हरशी कनेक्शन अयशस्वी",
  },
};

const DEMO_TEXT =
  "Kedarnath is a sacred town located in the Rudraprayag district of Uttarakhand, India, at an altitude of about 3,583 meters (11,755 feet) in the Garhwal Himalayas. It is one of the Char Dham pilgrimage sites and is dedicated to Lord Shiva.";

const QUICK_INFO = [
  { icon: "building", label: "State", value: "Uttarakhand" },
  { icon: "pin", label: "District", value: "Rudraprayag" },
  { icon: "mountain", label: "Altitude", value: "3,583 meters" },
  { icon: "city", label: "Nearest city", value: "Gaurikund" },
  { icon: "clock", label: "Best time to visit", value: "May to June & September to October" },
];

const nowTime = () =>
  new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });

/* the card opens with one sample question so it never looks empty */
const seed = () => [
  { id: "s1", from: "user", text: "Can you please tell me where is Kedarnath?", time: nowTime() },
  { id: "s2", from: "bot", demo: true, text: DEMO_TEXT, time: nowTime() },
];

export default function HeroChat({ language = "en", ask }) {
  const nav = useNavigate();
  const t = TXT[language] || TXT.en;

  const [messages, setMessages] = useState(seed);
  const [text, setText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [attached, setAttached] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const bodyRef = useRef(null);
  const recognitionRef = useRef(null);
  const synthRef = useRef(typeof window !== "undefined" ? window.speechSynthesis : null);
  const menuRef = useRef(null);

  /* ---------- keep the newest message in view (inside the card only) ---------- */
  useEffect(() => {
    if (messages.length <= 2 && !isTyping) return; // leave the opening view alone
    const el = bodyRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages.length, isTyping]);

  /* ---------- close the ⋮ menu when clicking elsewhere ---------- */
  useEffect(() => {
    if (!menuOpen) return;
    const close = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [menuOpen]);

  /* ---------- SEND MESSAGE (same backend call as the chat page) ---------- */
  const send = async (override) => {
    const raw = typeof override === "string" ? override : text;
    const imgPath = attached;
    const queryText = raw.trim() || (imgPath ? "Identify this attached photo" : "");
    if (!queryText && !imgPath) return;

    setMessages((m) => [
      ...m,
      { id: `u${Date.now()}`, from: "user", text: queryText, image_path: imgPath, time: nowTime() },
    ]);
    setText("");
    setAttached(null);
    setIsTyping(true);

    try {
      const data = await sendMessage(queryText, language, imgPath);
      setMessages((m) => [
        ...m,
        { id: `b${Date.now()}`, from: "bot", text: data.reply, audio_url: data.audio_url, time: nowTime() },
      ]);
    } catch (err) {
      console.error("HeroChat send error:", err);
      setMessages((m) => [
        ...m,
        { id: `e${Date.now()}`, from: "bot", text: t.error, time: nowTime() },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  /* ---------- a question tapped in the chips row ---------- */
  useEffect(() => {
    if (ask && ask.q) send(ask.q);
    // eslint-disable-next-line
  }, [ask]);

  /* ---------- FILE UPLOAD ---------- */
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setUploadSuccess(false);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API}/api/upload`, { method: "POST", body: formData });
      if (!res.ok) throw new Error("Server error");
      const data = await res.json();
      setAttached(data.filePath);
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 3000);
    } catch (err) {
      alert("Upload failed: " + err.message);
      console.error(err);
    } finally {
      setIsUploading(false);
      e.target.value = "";
    }
  };

  /* ---------- VOICE INPUT ---------- */
  const handleMic = () => {
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
      recognition.lang = LANG_MAP[language] || "en-US";
      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => setIsListening(true);
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) setText((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsListening(false);
      };
      recognition.onerror = (err) => {
        console.error("Speech recognition error:", err);
        setIsListening(false);
      };
      recognition.onend = () => setIsListening(false);

      recognition.start();
    } catch (err) {
      console.error("Failed to start mic:", err);
      setIsListening(false);
    }
  };

  /* ---------- READ ALOUD ---------- */
  const speak = (m) => {
    if (m.audio_url) {
      new Audio(`${API}${m.audio_url}`).play().catch((err) => console.error("Audio play failed:", err));
      return;
    }
    const synth = synthRef.current;
    if (!synth) return;
    const u = new SpeechSynthesisUtterance(m.text);
    u.lang = LANG_MAP[language] || "en-US";
    synth.cancel();
    synth.speak(u);
  };
  const stopSpeech = () => synthRef.current && synthRef.current.cancel();

  const imgSrc = (p) =>
    p.startsWith("http") ? p : `${API}/${p.replace(/\\/g, "/")}`;

  return (
    <aside className="hs-chat" aria-label="Chat with Deepshiva">
      {/* ---------- header ---------- */}
      <div className="hs-chat-head">
        <span className="hs-chat-logo">{Icon.trident(38)}</span>
        <div className="hs-chat-title">
          <div>
            <h3>Chat with Deepshiva</h3>
            <span className="hs-online"><i /> Online</span>
          </div>
          <p>Ask anything about Uttarakhand, temples, travel, rituals, culture...</p>
        </div>

        <div className="hs-menu-wrap" ref={menuRef}>
          <button
            type="button"
            className="hs-kebab"
            onClick={() => setMenuOpen((o) => !o)}
            aria-label="Chat options"
            aria-expanded={menuOpen}
          >
            {Icon.kebab(20)}
          </button>
          {menuOpen && (
            <div className="hs-menu" role="menu">
              <button type="button" role="menuitem" onClick={() => nav("/chat")}>
                {Icon.chat(16)} Open full chat
              </button>
              <button
                type="button"
                role="menuitem"
                onClick={() => {
                  setMessages(seed());
                  setMenuOpen(false);
                }}
              >
                {Icon.trash(16)} Clear chat
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ---------- messages ---------- */}
      <div className="hs-chat-body" ref={bodyRef}>
        {messages.map((m) =>
          m.from === "user" ? (
            <div className="hs-msg-user" key={m.id}>
              <div className="hs-bubble-user">
                {m.image_path && <img className="hs-user-img" src={imgSrc(m.image_path)} alt="Your upload" />}
                {m.text}
                <time>{m.time}</time>
              </div>
              <span className="hs-avatar-user">{Icon.user(20)}</span>
            </div>
          ) : (
            <div className="hs-msg-bot" key={m.id}>
              <span className="hs-avatar-bot"><Logo /></span>
              <div className="hs-bubble-bot">
                {m.demo ? (
                  <>
                    <div className="hs-bot-top">
                      <p>{m.text}</p>
                      <img src={kedarnathImg} alt="Kedarnath temple" />
                    </div>
                    <strong className="hs-quick-title">Quick Info:</strong>
                    <ul className="hs-quick">
                      {QUICK_INFO.map((q) => (
                        <li key={q.label}>
                          <span className="hs-quick-ic">{Icon[q.icon](16)}</span>
                          {q.label}: {q.value}
                        </li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <p className="hs-reply">{m.text}</p>
                )}

                {/* 🧘 audio sent by the server */}
                {m.audio_url && (
                  <div className="hs-audio">
                    <audio controls autoPlay src={`${API}${m.audio_url}`}>
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                )}

                <div className="hs-bot-foot">
                  {!m.audio_url && (
                    <span className="hs-tts">
                      <button type="button" onClick={() => speak(m)} title="Listen" aria-label="Listen">
                        {Icon.speaker(15)}
                      </button>
                      <button type="button" className="stop" onClick={stopSpeech} title="Stop" aria-label="Stop">
                        {Icon.stop(15)}
                      </button>
                    </span>
                  )}
                  <time>{m.time}</time>
                </div>
              </div>
            </div>
          )
        )}

        {isTyping && (
          <div className="hs-msg-bot">
            <span className="hs-avatar-bot"><Logo /></span>
            <div className="hs-bubble-bot hs-typing" role="status">
              <span className="hs-dots" aria-hidden="true"><i /><i /><i /></span>
              <span>{t.typing}</span>
            </div>
          </div>
        )}
      </div>

      {/* ---------- attached image chip ---------- */}
      {attached && (
        <div className="hs-attach" role="status">
          <span className="hs-attach-ic">{Icon.image(16)}</span>
          <span className="hs-attach-name">Photo attached: {attached.split(/[\\/]/).pop()}</span>
          <button type="button" onClick={() => setAttached(null)} aria-label="Remove image">
            {Icon.close(14)}
          </button>
        </div>
      )}

      {/* ---------- input ---------- */}
      <div className="hs-chat-input">
        <div className={`hs-input-pill ${isListening ? "is-listening" : ""}`}>
          <label className="hs-input-btn" title="Attach image">
            {isUploading ? <span className="hs-spin" /> : uploadSuccess ? Icon.check(22) : Icon.image(22)}
            <input type="file" accept="image/*" hidden onChange={handleFileChange} disabled={isUploading} />
          </label>

          <input
            className="hs-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder={isListening ? "Listening..." : t.placeholder}
            aria-label="Message"
          />

          <button
            type="button"
            className={`hs-input-btn ${isListening ? "listening" : ""}`}
            onClick={handleMic}
            title={isListening ? "Stop Listening" : "Speak with Mic"}
            aria-label={isListening ? "Stop Listening" : "Speak with Mic"}
          >
            {Icon.mic(20)}
          </button>
        </div>

        <button type="button" className="hs-send" onClick={() => send()} aria-label="Send message">
          {Icon.send(24)}
        </button>
      </div>
    </aside>
  );
}