import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function EntryForm() {
  const navigate = useNavigate();

  const [country, setCountry] = useState("");
  const [continent, setContinent] = useState("");
  const [year, setYear] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!country && !continent) {
      alert("Please enter either a country or a continent.");
      return;
    }

    const finalContinent = country && continent ? "N/A" : continent;

    navigate("/results", {
      state: {
        country,
        continent: finalContinent,
        year,
      },
    });
  };

  return (
    <div className="page fade-in">
      <h1 style={{ color: "var(--primary-green)", marginBottom: "20px" }}>
        Enter Your Details
      </h1>

      <form
        onSubmit={handleSubmit}
        style={{ width: "100%", maxWidth: "400px", margin: "0 auto" }}
      >
        <input
          type="text"
          placeholder="Country (optional)"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />

        <input
          type="text"
          placeholder="Continent (optional)"
          value={continent}
          onChange={(e) => setContinent(e.target.value)}
        />

        <input
          type="number"
          placeholder="Year (required)"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          required
        />

        <button type="submit">Predict</button>
      </form>
    </div>
  );
}
