import { useLocation } from "react-router-dom";

export default function Results() {
  const { state } = useLocation();

  const country = state?.country || "N/A";
  const year = state?.year || "N/A";
  const salary = state?.salary || "N/A";
  const commodities = state?.commodities || [];

  return (
    <div className="page fade-in results-page">

      <h1 className="results-title">Predicted Results</h1>

      <div className="results-section">
        <h2 className="results-header">Country</h2>
        <p className="results-value">{country}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Year</h2>
        <p className="results-value">{year}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Salary</h2>
        <p className="results-value">{salary}</p>
      </div>

      <div className="results-section">
        <h2 className="results-header">Top Commodities</h2>

        <div className="results-list">
          {commodities.length > 0 ? (
            commodities.map((item, index) => (
              <p key={index} className="results-value">{item}</p>
            ))
          ) : (
            <p className="results-value">No data available</p>
          )}
        </div>
      </div>

    </div>
  );
}
