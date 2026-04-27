import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

export default function Results() {
  const { state } = useLocation();

  const year = state?.year || "N/A";
  const country = state?.country || "N/A";
  const continent = state?.continent || "N/A";
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const apiBaseUrl = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000";

  useEffect(() => {
    if (!state?.year) {
      setError("Missing input details. Please go back and submit the form again.");
      setLoading(false);
      return;
    }

    const payload = {
      year: Number(state.year),
      country: state.country?.trim() || null,
      continent:
        state.country?.trim() || !state.continent || state.continent === "N/A"
          ? null
          : state.continent.trim(),
    };

    const fetchPrediction = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${apiBaseUrl}/predict`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
          const message = Array.isArray(data.error) ? data.error.join(" ") : data.error;
          throw new Error(message || "Failed to get prediction.");
        }

        setPrediction(data);
      } catch (err) {
        setError(err.message || "Could not connect to backend.");
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, [apiBaseUrl, state]);

  return (
    <div className="page fade-in results-page">

      <h1 className="results-title">Predicted Results</h1>

      <div className="results-section">
        <h2 className="results-header">Year</h2>
        <p className="results-value">{year}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Country</h2>
        <p className="results-value">{country}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Continent</h2>
        <p className="results-value">{continent}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">CPI</h2>
        <p className="results-value">
          {loading
            ? "Loading..."
            : prediction
              ? `${prediction.cpi_change}%`
              : "—"}
        </p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Healthy Diet Cost</h2>
        <p className="results-value">
          {loading
            ? "Loading..."
            : prediction
              ? `$${Number(prediction.annual_cost_healthy_diet).toLocaleString()} / year`
              : "—"}
        </p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Healthy Fruit & Vegetable Cost</h2>
        <p className="results-value">
          {loading
            ? "Loading..."
            : prediction
              ? `$${Number(prediction.annual_cost_fruits_and_veg).toLocaleString()} / year`
              : "—"}
        </p>
      </div>

      {error && (
        <div className="results-section">
          <h2 className="results-header">Error</h2>
          <p className="results-value">{error}</p>
        </div>
      )}

    </div>
  );
}
