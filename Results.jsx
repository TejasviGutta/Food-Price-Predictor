import { useLocation } from "react-router-dom";

export default function Results() {
  const { state } = useLocation();

  const year = state?.year || "N/A";
  const country = state?.country || "N/A";
  const continent = state?.continent || "N/A";

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
          (Consumer Price Index) measures inflation
        </p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Healthy Diet Cost</h2>
        <p className="results-value">—</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Healthy Fruit & Vegetable Cost</h2>
        <p className="results-value">—</p>
      </div>

    </div>
  );
}
