import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import SplashScreen from "./SplashScreen";
import Welcome from "./Welcome";
import EntryForm from "./EntryForm";
import Results from "./Results";

export default function App() {
  const [showContent, setShowContent] = useState(false);

  return (
    <Router>
      {/* Splash animation */}
      <SplashScreen onMoveUp={() => setShowContent(true)} />

      {/* Only show routes AFTER splash finishes */}
      {showContent && (
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/entry" element={<EntryForm />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      )}
    </Router>
  );
}
