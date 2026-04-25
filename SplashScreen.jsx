import { useEffect, useState } from "react";

export default function SplashScreen({ onMoveUp }) {
  const [moveUp, setMoveUp] = useState(false);

  useEffect(() => {
    // Zoom in (1s) + pause (1s)
    const startSlide = setTimeout(() => {
      setMoveUp(true);
      onMoveUp(); // load content immediately
    }, 2000);

    return () => clearTimeout(startSlide);
  }, [onMoveUp]);

  return (
    <div className={`splash-screen ${moveUp ? "move-up" : ""}`}>
      <h1 className="splash-title">FoodForecast</h1>
    </div>
  );
}
