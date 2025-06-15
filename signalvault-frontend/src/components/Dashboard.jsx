import React, { useState } from 'react';
import './Dashboard.css';

export default function Dashboard() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setResult(`Analyzing: ${query}...`);

    try {
      const res = await fetch('http://localhost:5000/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ query })
      });
      const data = await res.text(); // or await res.json() if you're using JSON
      setResult(data);
    } catch (err) {
      setResult('❌ Something went wrong.');
    }
  };

  return (
    <div>
      <h1>SignalVault Dashboard</h1>
      <div className="dashboard">
        <div className="card">
          <h2>Search Keyword</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <input
                type="text"
                placeholder="Type a topic..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
              />
              <button type="submit">Analyze</button>
            </div>
            <div className="result">{result || 'Enter a keyword to begin analysis.'}</div>
          </form>
        </div>

        <div className="card">
          <h2>Trend Visualization</h2>
          <div id="trend-graph">
            <p className="result">Graph data will appear here.</p>
          </div>
        </div>
      </div>
    </div>
  );
}