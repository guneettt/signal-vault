import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("Try typing a medical emergency keyword.");

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setStatus(`Searching for "${query}"...`);
    setResults([]);

    try {
      const response = await fetch("http://localhost:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error("Non-200 response");

      const data = await response.json();

      if (data.emergency) {
        setStatus(`🚨 Emergency protocol: ${data.query}`);
        setResults(
          data.checklist.map((tip, i) => ({
            filename: `Emergency Step #${i + 1}`,
            score: "",
            snippet: tip,
          }))
        );
      } else {
        setStatus(`Showing results for "${data.query}"`);
        setResults(data.results);
      }
    } catch (err) {
      console.error("Error:", err);
      setStatus("❌ Could not fetch results.");
    }
  };

  const emergencyKeywords = [
    "can't find water",
    "earthquake",
    "stuck in flood",
    "unclear breathing",
    "fire in building",
  ];

  const handleEmergencyClick = (term) => {
    setQuery(term);
    setTimeout(() => handleSearch(), 100); // ensure query is updated before sending
  };

  return (
    <div className="container">
      <h1>SignalVault Dashboard</h1>
      <form className="search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search emergency keywords..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      <p className="status">{status}</p>

      <div className="main-content">
        <div className="results">
          {results.map((res, idx) => (
            <div className="result-card" key={idx}>
              <h3>📄 {res.filename}</h3>
              {res.score && <p className="score">Score: {res.score}</p>}
              <p className="snippet">{res.snippet}</p>
            </div>
          ))}
        </div>

        <div className="emergency-box">
          <h4>Emergency Situations</h4>
          {emergencyKeywords.map((term, i) => (
            <button
              key={i}
              className="emergency-btn"
              onClick={() => handleEmergencyClick(term)}
            >
              {term}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
