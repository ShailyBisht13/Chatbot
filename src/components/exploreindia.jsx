import React, { useState } from "react";
import "./exploreindia.css";

const states = [
  "Uttarakhand", "Uttar Pradesh", "Himachal Pradesh", "Jammu & Kashmir",
  "Delhi", "Maharashtra", "Tamil Nadu", "Kerala", "Karnataka", "Goa",
  "Rajasthan", "Assam", "Sikkim", "Bihar", "West Bengal"
];

const territories = [
  "Andaman & Nicobar", "Chandigarh", "Delhi (NCT)",
  "Ladakh", "Lakshadweep", "Puducherry", "Daman & Diu"
];

const themes = ["Spiritual", "Wellness / Yoga", "Eco-Trek", "Heritage", "Adventure"];

export default function ExploreIndia() {
  const [selectedState, setSelectedState] = useState("");
  const [selectedUT, setSelectedUT] = useState("");
  const [selectedTheme, setSelectedTheme] = useState("");

  return (
    <div className="explore-container">
      <h1 className="explore-title">Explore India with DeepShiva</h1>
      <p className="explore-subtitle">Choose your travel preferences to discover attractions.</p>

      {/* STATE DROPDOWN */}
      <div className="dropdown-box">
        <label>Select a State</label>
        <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)}>
          <option value="">-- Choose State --</option>
          {states.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* UT DROPDOWN */}
      <div className="dropdown-box">
        <label>Select a Union Territory</label>
        <select value={selectedUT} onChange={(e) => setSelectedUT(e.target.value)}>
          <option value="">-- Choose UT --</option>
          {territories.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>

      {/* THEME DROPDOWN */}
      <div className="dropdown-box">
        <label>Select a Theme</label>
        <select value={selectedTheme} onChange={(e) => setSelectedTheme(e.target.value)}>
          <option value="">-- Choose Theme --</option>
          {themes.map((theme) => (
            <option key={theme} value={theme}>{theme}</option>
          ))}
        </select>
      </div>

      {/* SHOW RESULT */}
      <div className="result-card">
        <h2>Your Selection</h2>
        <p><strong>State:</strong> {selectedState || "Not selected"}</p>
        <p><strong>UT:</strong> {selectedUT || "Not selected"}</p>
        <p><strong>Theme:</strong> {selectedTheme || "Not selected"}</p>
      </div>
    </div>
  );
}
