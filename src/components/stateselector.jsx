import React from "react";
import "./stateselector.css";

const STATES = [
  "Uttarakhand",
  "Uttar Pradesh",
  "Himachal Pradesh",
  "Jammu & Kashmir",
  "Delhi",
  "Maharashtra",
  "Gujarat",
  "Rajasthan",
  "Goa",
  "Tamil Nadu",
  "Kerala",
  "Karnataka",
  "Telangana",
  "Andhra Pradesh",
  "Madhya Pradesh",
  "Bihar",
  "West Bengal",
  "Assam",
  "Sikkim",
  "Meghalaya",
  // ...add upto 36 as needed
];

function StateSelector({ onSelect }) {
  return (
    <div className="state-selector">
      <h3>Select a State / UT</h3>
      <div className="state-grid">
        {STATES.map((s) => (
          <button key={s} onClick={() => onSelect(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

export default StateSelector;
