import React from "react";
import { useNavigate } from "react-router-dom";

export default function HomeScreen() {
  const nav = useNavigate();

  const bgUrl =
    "https://static.vecteezy.com/system/resources/previews/022/540/430/large_2x/kedarnath-temple-mountains-free-photo.jpg";

  return (
    <div
      style={{
        height: "100vh",
        backgroundImage: `url(${bgUrl})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
      }}
    >
      {/* DARK OVERLAY FOR READABILITY */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "rgba(0,0,0,0.55)",
        }}
      />

      <div style={{ position: "relative", zIndex: 1, textAlign: "center" }}>
        <h1
          style={{
            color: "#ffdd99",
            fontSize: "48px",
            textShadow: "0 0 18px #000",
            marginBottom: "10px",
          }}
        >
          🕉️ DeepShiva
        </h1>

        <p
          style={{
            color: "white",
            fontSize: "20px",
            marginBottom: "30px",
            opacity: 0.9,
          }}
        >
          Spiritual Tourism & Himalayan Wisdom
        </p>

        <button
          onClick={() => nav("/chat")}
          style={btnStyle}
        >
          Start Chatbot
        </button>

        <button
          onClick={() => nav("/explore")}
          style={{ ...btnStyle, background: "#34d399" }}
        >
          Explore India
        </button>
      </div>
    </div>
  );
}

const btnStyle = {
  padding: "14px 28px",
  borderRadius: "12px",
  fontSize: "18px",
  border: "none",
  cursor: "pointer",
  margin: "10px",
  background: "#fbbf24",
  color: "#000",
  fontWeight: "bold",
  boxShadow: "0 0 15px rgba(255,200,100,0.7)",
};
