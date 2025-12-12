import React, { useState } from "react";
import "./explorepage.css";
import ExploreIndia from "../components/exploreindia";
import StateSelector from "../components/stateselector";
import ThemeSelector from "../components/themeselector";

function ExplorePage() {
  const [selectedState, setSelectedState] = useState(null);
  const [selectedTheme, setSelectedTheme] = useState(null);

  return (
    <div className="explore-root">
      <div className="explore-inner">
        <h1>Explore India with DeepShiva</h1>

        <ExploreIndia
          onStates={() => {}}
          onThemes={() => {}}
        />

        <StateSelector onSelect={(s) => setSelectedState(s)} />
        <ThemeSelector onSelect={(t) => setSelectedTheme(t)} />

        <div className="explore-selection">
          {selectedState && (
            <p>
              Selected State: <strong>{selectedState}</strong>
            </p>
          )}
          {selectedTheme && (
            <p>
              Selected Theme: <strong>{selectedTheme}</strong>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ExplorePage;
