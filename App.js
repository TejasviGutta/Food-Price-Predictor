import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import SplashScreen from "./components/SplashScreen";
import Welcome from "./pages/Welcome";
import EntryForm from "./pages/EntryForm";
import Results from "./pages/Results";

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
