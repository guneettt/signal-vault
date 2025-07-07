import React, { useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import FlowChart from "./FlowChart";

function Dashboard() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("Try typing a medical emergency keyword.");
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setStatus(`Searching for "${query}"...`);
    setResults([]);

    try {
      const response = await fetch("http://localhost:5050/", {
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
            isEmergency: true,
          }))
        );
      } else {
        setStatus(`Showing results for "${data.query}"`);
        const filtered = data.results
          .filter(r => r.flowstep_count && r.flowstep_count > 0)
          .map(r => ({ ...r, isEmergency: false }));

        setResults(filtered);
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
    "trapped under rubble",
    "injured with bleeding",
    "lost in forest",
  ];

  const handleEmergencyClick = (term) => {
    setQuery(term);
    setTimeout(() => handleSearch(), 100);
  };

  const handleResultClick = (filename) => {
    navigate(`/flow/${encodeURIComponent(filename)}?query=${encodeURIComponent(query)}`);
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
            <div
              className="result-card"
              key={idx}
              onClick={() => !res.isEmergency && handleResultClick(res.filename)}
              style={{ cursor: res.isEmergency ? "default" : "pointer" }}
            >
              <h3>{res.isEmergency ? "🚑" : "📄"} {res.filename}</h3>
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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/flow/:filename" element={<FlowChart />} />
      </Routes>
    </Router>
  );
}

export default App;
