import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Icon, Logo } from "../components/homeicons";
import "./helppage.css";

const FEATURES = [
  { icon: "temple", text: "Spiritual guidance & temple information" },
  { icon: "mountain", text: "Tourism assistance for Himalayan regions" },
  { icon: "pin", text: "Nearby temples & sacred places" },
  { icon: "lotus", text: "Guided meditation & mindfulness" },
  { icon: "book", text: "Festivals, rituals & cultural knowledge" },
  { icon: "speaker", text: "Audio guidance & chants" },
  { icon: "mic", text: "Voice-based interaction" },
  { icon: "globe", text: "Multilingual support (English & Hindi)" },
  { icon: "compass", text: "Travel tips & local insights" },
  { icon: "clock", text: "Best time to visit spiritual places" },
];

export default function HelpPage() {
  const navigate = useNavigate();

  return (
    <div className="help-container">
      {/* ---------- top bar ---------- */}
      <div className="help-bar">
        <Link to="/" className="help-brand" aria-label="Deepshiva home">
          <Logo />
          <span>
            <strong>Deepshiva</strong>
            <small>Spiritual Tourism &amp; Himalayan Wisdom</small>
          </span>
        </Link>

        <Link to="/" className="help-home">
          Home
        </Link>
      </div>

      <header className="help-hero">
        <h1>
          How <em>DeepShiva</em> Helps You
        </h1>
        <p className="help-subtitle">
          An AI-powered assistant for spiritual tourism, guidance, and cultural
          exploration
        </p>
      </header>

      {/* ALL FEATURES IN SAME GRID */}
      <div className="help-grid">
        {FEATURES.map((f, i) => (
          <div className="help-card" key={f.text} style={{ "--i": i }}>
            <span className="help-icon" aria-hidden="true">
              {Icon[f.icon](26)}
            </span>
            <span className="help-text">{f.text}</span>
          </div>
        ))}
      </div>

      {/* START CHAT */}
      <div className="help-card-wrapper">
        <button
          type="button"
          className="help-cta"
          onClick={() => navigate("/chat")}
        >
          {Icon.chat(20)}
          <span>Start Chat with DeepShiva</span>
          {Icon.arrow(20)}
        </button>
      </div>

      <div className="help-footer">
        <p>
          DeepShiva is designed to make spiritual journeys easier, meaningful,
          and accessible for everyone.
        </p>
      </div>
    </div>
  );
}