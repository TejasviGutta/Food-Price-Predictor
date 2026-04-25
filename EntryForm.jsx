import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function EntryForm() {
  const navigate = useNavigate();

  const [country, setCountry] = useState("");
  const [year, setYear] = useState("");
  const [salary, setSalary] = useState("");
  const [commodities, setCommodities] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    const commodityList = commodities
      .split(",")
      .map((item) => item.trim())
      .filter((item) => item.length > 0);

    navigate("/results", {
      state: {
        country,
        year,
        salary,
        commodities: commodityList,
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
          placeholder="Country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="Salary (optional)"
          value={salary}
          onChange={(e) => setSalary(e.target.value)}
        />

        <input
          type="text"
          placeholder="Top commodities (comma separated)"
          value={commodities}
          onChange={(e) => setCommodities(e.target.value)}
          required
        />

        <button type="submit">Predict</button>
      </form>
    </div>
  );
}
