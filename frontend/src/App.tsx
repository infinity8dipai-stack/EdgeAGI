import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Nodes from './pages/Nodes';
import Tasks from './pages/Tasks';
import Credits from './pages/Credits';
import Settings from './pages/Settings';
import './styles/index.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="logo">
            <h1>EdgeAGI</h1>
            <p>Decentralized AI Swarm</p>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/nodes">Nodes</Link></li>
            <li><Link to="/tasks">Tasks</Link></li>
            <li><Link to="/credits">Credits</Link></li>
            <li><Link to="/settings">Settings</Link></li>
          </ul>
          <div className="status-indicator">
            <span className="status-dot online"></span>
            <span>Connected</span>
          </div>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/nodes" element={<Nodes />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/credits" element={<Credits />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
