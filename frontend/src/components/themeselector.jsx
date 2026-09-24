import React from "react";
import "./themeselector.css";

const THEMES = [
  { id: "spiritual", label: "Spiritual" },
  { id: "wellness", label: "Wellness / Yoga" },
  { id: "eco_trek", label: "Eco-Trek" },
];

function ThemeSelector({ onSelect }) {
  return (
    <div className="theme-selector">
      <h3>Select a Theme</h3>
      <div className="theme-row">
        {THEMES.map((t) => (
          <button key={t.id} onClick={() => onSelect(t.id)}>
            {t.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ThemeSelector;
