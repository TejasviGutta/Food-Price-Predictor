import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="page fade-in">
      <h1 style={{ color: "var(--primary-green)", marginBottom: "10px" }}>
        Welcome to FoodForecast
      </h1>

      <p style={{ maxWidth: "500px", margin: "0 auto 20px", lineHeight: "1.6" }}>
        Predict future food prices based on your country, year, salary, and top commodities.
      </p>

      <button onClick={() => navigate("/entry")}>
        Get Started
      </button>
    </div>
  );
}
