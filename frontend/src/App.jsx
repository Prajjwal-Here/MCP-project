import React, { useState } from 'react';
import Search from './components/Search';
import Compare from './components/Compare';
import Strategy from './components/Strategy';
import TeamBuilder from './components/TeamBuilder';
import './style.css';

function App() {
  const [selectedModule, setSelectedModule] = useState('');

  return (
    <div className="app-container">
      <h1 className="main-title">🎮 MCP Pokémon Interface</h1>
      
      <div className="module-selector">
        <label>Choose a Module:</label>
        <select value={selectedModule} onChange={(e) => setSelectedModule(e.target.value)}>
          <option value="">-- Select --</option>
          <option value="search">Search Info</option>
          <option value="compare">Compare Pokémon</option>
          <option value="strategy">Strategy Suggestion</option>
          <option value="team">Generate Team</option>
        </select>
      </div>

      <div className="module-box">
        {selectedModule === 'search' && <Search />}
        {selectedModule === 'compare' && <Compare />}
        {selectedModule === 'strategy' && <Strategy />}
        {selectedModule === 'team' && <TeamBuilder />}
      </div>
    </div>
  );
}

export default App;
