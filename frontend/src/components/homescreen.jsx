import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./homescreen.css";
import { Icon, Logo } from "./homeicons";
import HeroChat from "./herochat";

/* ---------- IMAGES (put these in src/assets/) ---------- */
import heroBg from "../assets/hero.png";
import kedarnathImg from "../assets/kedarnath.jpg";
import badrinathImg from "../assets/badrinath.png";
import gangotriImg from "../assets/gangotri.jpg";
import yamunotriImg from "../assets/yamunotri.jpg";
import rishikeshImg from "../assets/rishikesh.jpg";
import haridwarImg from "../assets/haridwar.jpg";

/* ---------- CONTENT ---------- */
const HERO_POINTS = [
  { icon: "temple", lines: ["Sacred", "Destinations"] },
  { icon: "route", lines: ["Yatra Planning", "& Routes"] },
  { icon: "lotus", lines: ["Spiritual", "Guidance"] },
];

const CHIPS = [
  { icon: "route", lines: ["How to reach", "Kedarnath?"] },
  { icon: "calendar", lines: ["Best time for", "Char Dham Yatra?"] },
  { icon: "pin", lines: ["Distance from", "Rishikesh to Badrinath?"] },
  { icon: "temple", lines: ["What are the rituals", "at Kedarnath?"] },
  { icon: "doc", lines: ["Show me a 7-day", "yatra plan"] },
  { icon: "book", lines: ["Tell me about", "Uttarakhand culture"] },
];

const DESTINATIONS = [
  { name: "Kedarnath", tag: "Abode of Lord Shiva", img: kedarnathImg },
  { name: "Badrinath", tag: "Gateway to Salvation", img: badrinathImg },
  { name: "Gangotri", tag: "Origin of River Ganga", img: gangotriImg },
  { name: "Yamunotri", tag: "Source of River Yamuna", img: yamunotriImg },
  { name: "Rishikesh", tag: "Yoga, Peace & Adventure", img: rishikeshImg },
  { name: "Haridwar", tag: "Gateway to the Gods", img: haridwarImg },
];

const FEATURES = [
  { icon: "chat", title: "Instant Answers", desc: "About destinations, routes, rituals & more" },
  { icon: "map", title: "Personalized Yatra Plans", desc: "Based on your time and preferences" },
  { icon: "cloudsun", title: "Live Weather Updates", desc: "Get real-time weather for all destinations" },
  { icon: "book", title: "Mythology & Stories", desc: "Discover the cultural and spiritual heritage" },
  { icon: "lotus", title: "Meditation & Yoga", desc: "Guided meditation audios for peace" },
  { icon: "compass", title: "Local Travel Tips", desc: "Stay, food, transport and safety information" },
];

export default function HomeScreen() {
  const nav = useNavigate();
  const destRef = useRef(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [ask, setAsk] = useState(null); // question sent from a chip to the bot
  const [lang, setLang] = useState(() => localStorage.getItem("ds_language") || "en");

  const scrollTo = (ref) => {
    setMenuOpen(false);
    ref.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  const go = (path) => {
    setMenuOpen(false);
    nav(path);
  };
  const changeLang = (e) => {
    setLang(e.target.value);
    localStorage.setItem("ds_language", e.target.value);
  };

  /* nav links */
  const LINKS = [
    { label: "Home", active: true, onClick: () => window.scrollTo({ top: 0, behavior: "smooth" }) },
    { label: "Chat", onClick: () => go("/chat") },
    { label: "Destinations", onClick: () => scrollTo(destRef) },
    { label: "About", onClick: () => go("/help") },
  ];

  return (
    <div className="hs">
      {/* ================= HERO ================= */}
      <section className="hs-hero" style={{ backgroundImage: `url(${heroBg})` }}>
        <div className="hs-hero-shade" />

        {/* ---------- NAV ---------- */}
        <header className="hs-nav">
          <button className="hs-logo" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })} aria-label="Deepshiva home">
            <Logo />
            <span className="hs-logo-text">
              <strong>Deepshiva</strong>
              <small>Spiritual Tourism &amp; Himalayan Wisdom</small>
            </span>
          </button>

          <nav className="hs-links" aria-label="Main">
            {LINKS.map((l) => (
              <button key={l.label} className={l.active ? "active" : ""} onClick={l.onClick}>
                {l.label}
              </button>
            ))}
          </nav>

          <div className="hs-nav-right">
            <button className="hs-icon-btn" onClick={() => go("/chat")} aria-label="Search in chat">
              {Icon.search(20)}
            </button>

            <label className="hs-lang">
              {Icon.globe(18)}
              <select value={lang} onChange={changeLang} aria-label="Language">
                <option value="en">EN</option>
                <option value="hi">HI</option>
                <option value="bn">BN</option>
                <option value="mr">MR</option>
              </select>
              {Icon.chevron(14)}
            </label>

            <button className="hs-login" onClick={() => go("/login")}>Login</button>

            <button className="hs-plan" onClick={() => go("/chat")}>
              {Icon.temple(20)}
              <span>Plan Your Yatra</span>
              {Icon.arrow(18)}
            </button>

            <button
              className="hs-icon-btn hs-burger"
              onClick={() => setMenuOpen((o) => !o)}
              aria-label="Menu"
              aria-expanded={menuOpen}
            >
              {menuOpen ? Icon.close(24) : Icon.menu(24)}
            </button>
          </div>
        </header>

        {menuOpen && (
          <div className="hs-mobile-menu">
            {LINKS.map((l) => (
              <button key={l.label} onClick={l.onClick}>{l.label}</button>
            ))}
            <button onClick={() => go("/login")}>Login</button>
          </div>
        )}

        {/* ---------- HERO CONTENT ---------- */}
        <div className="hs-hero-grid">
          <div className="hs-hero-left">
            <span className="hs-badge">
              {Icon.sparkle(16)} AI-Powered Spiritual Travel Guide
            </span>

            <h1>
              Ask <em>Deepshiva</em>
            </h1>
            <h2>
              Your AI companion for Spiritual Tourism &amp; Himalayan Wisdom
            </h2>
            <p>
              Get instant answers about destinations, yatra routes, rituals,
              weather, travel tips, mythology, and more. Explore the divine
              beauty of Uttarakhand with AI.
            </p>

            <div className="hs-points">
              {HERO_POINTS.map((p) => (
                <div className="hs-point" key={p.icon}>
                  <span className="hs-ring">{Icon[p.icon](28)}</span>
                  <span>
                    {p.lines[0]}
                    <br />
                    {p.lines[1]}
                  </span>
                </div>
              ))}
            </div>

            <button className="hs-cta" onClick={() => go("/chat")}>
              Start Chatting {Icon.arrow(20)}
            </button>
          </div>

          {/* ---------- WORKING CHATBOT ---------- */}
          <HeroChat language={lang} ask={ask} />
        </div>

        {/* ---------- QUESTION CHIPS ---------- */}
        <div className="hs-chips">
          {CHIPS.map((c) => (
            <button
              key={c.lines.join(" ")}
              className="hs-chip"
              onClick={() => setAsk({ q: c.lines.join(" "), n: Date.now() })}
            >
              <span className="hs-chip-ic">{Icon[c.icon](30)}</span>
              <span className="hs-chip-text">
                {c.lines[0]}
                <br />
                {c.lines[1]}
              </span>
              <span className="hs-chip-arrow">{Icon.arrow(16)}</span>
            </button>
          ))}
        </div>
      </section>

      {/* ================= POPULAR DESTINATIONS ================= */}
      <section className="hs-dest" ref={destRef}>
        <div className="hs-section-head">
          <h2>Popular Destinations</h2>
          <button onClick={() => go("/chat")}>
            View All Destinations {Icon.arrow(18)}
          </button>
        </div>

        <div className="hs-dest-grid">
          {DESTINATIONS.map((d) => (
            <button key={d.name} className="hs-card" onClick={() => go("/chat")}>
              <img src={d.img} alt={d.name} loading="lazy" />
              <span className="hs-card-shade" />
              <span className="hs-card-info">
                <span>
                  <strong>{d.name}</strong>
                  <small>{d.tag}</small>
                </span>
                <span className="hs-card-go">{Icon.arrow(14)}</span>
              </span>
            </button>
          ))}
        </div>
      </section>

      {/* ================= MORE THAN A CHATBOT ================= */}
      <section className="hs-more" style={{ backgroundImage: `url(${heroBg})` }}>
        <div className="hs-more-shade" />
        <span className="hs-om" aria-hidden="true">ॐ</span>

        <div className="hs-more-inner">
          <h2>
            More Than <em>a Chatbot</em>
          </h2>
          <p className="hs-more-sub">Your complete spiritual travel companion</p>

          <div className="hs-feat-grid">
            {FEATURES.map((f) => (
              <div className="hs-feat" key={f.title}>
                <span className="hs-ring">{Icon[f.icon](26)}</span>
                <strong>{f.title}</strong>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}