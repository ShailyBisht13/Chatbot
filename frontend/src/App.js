import { Routes, Route } from "react-router-dom";

import HomeScreen from "./components/homescreen";
import ChatPage from "./pages/chatpage";
import HelpPage from "./pages/helppage";
import Login from "./pages/login";
import Signup from "./pages/signup";

/* ---------- TEMPORARY CHECK (delete once the error is gone) ----------
   Prints in the browser console (F12) which import is not a valid
   React component, so you know exactly which file to fix. */
Object.entries({ HomeScreen, ChatPage, HelpPage, Login, Signup }).forEach(
  ([name, comp]) => {
    const valid =
      typeof comp === "function" || (comp && typeof comp === "object" && comp.$$typeof);
    if (!valid) {
      console.error(
        `❌ "${name}" is not a valid component (got ${typeof comp}). ` +
          `Check that its file has "export default" and that the import path/name is correct.`,
        comp
      );
    }
  }
);

function App() {
  return (
    <Routes>
      {/* Home page */}
      <Route path="/" element={<HomeScreen />} />

      {/* Chat page */}
      <Route path="/chat" element={<ChatPage />} />

      {/* How DeepShiva Helps page */}
      <Route path="/help" element={<HelpPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
    </Routes>
  );
}

export default App;