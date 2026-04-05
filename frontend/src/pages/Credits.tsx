import React, { useState, useEffect } from 'react';
import { getCredits } from '../services/api';

interface Credit {
  node_id: string;
  balance: number;
  earned: number;
  spent: number;
  last_updated: string;
}

const Credits: React.FC = () => {
  const [credits, setCredits] = useState<Credit | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCredits();
  }, []);

  const loadCredits = async () => {
    try {
      // In a real app, you'd pass the actual node ID
      const response = await getCredits('default-node');
      setCredits(response.data);
    } catch (error) {
      console.error('Failed to load credits:', error);
      // Set mock data for demo
      setCredits({
        node_id: 'default-node',
        balance: 150,
        earned: 200,
        spent: 50,
        last_updated: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h2>Credits</h2>
        <p>Rewards and credit ledger for compute contributions</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Current Balance</h3>
          <div className="value">{credits?.balance || 0}</div>
          <div className="change">EGC Tokens</div>
        </div>
        <div className="stat-card">
          <h3>Total Earned</h3>
          <div className="value">{credits?.earned || 0}</div>
          <div className="change">From compute tasks</div>
        </div>
        <div className="stat-card">
          <h3>Total Spent</h3>
          <div className="value">{credits?.spent || 0}</div>
          <div className="change">On task execution</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>About EdgeAGI Credits</h3>
        </div>
        <div style={{ color: 'var(--text-secondary)', lineHeight: '1.8' }}>
          <p style={{ marginBottom: '1rem' }}>
            EdgeAGI Credits (EGC) are reward tokens earned by contributing your idle 
            CPU/GPU resources to the decentralized AI swarm network.
          </p>
          <h4 style={{ margin: '1.5rem 0 0.75rem', color: 'var(--text-primary)' }}>How to Earn Credits:</h4>
          <ul style={{ marginLeft: '1.5rem', marginBottom: '1.5rem' }}>
            <li>Register your node to the network</li>
            <li>Keep your node online and available</li>
            <li>Complete assigned AI inference tasks</li>
            <li>Contribute GPU resources for training jobs</li>
          </ul>
          <h4 style={{ margin: '1.5rem 0 0.75rem', color: 'var(--text-primary)' }}>How to Spend Credits:</h4>
          <ul style={{ marginLeft: '1.5rem', marginBottom: '1.5rem' }}>
            <li>Submit your own AI tasks to the swarm</li>
            <li>Prioritize your tasks with higher rewards</li>
            <li>Access premium models and features</li>
          </ul>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Note: This is a demonstration of the credit system. In production, EGC tokens 
            would be implemented on a blockchain or distributed ledger.
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Recent Transactions</h3>
        </div>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Type</th>
                <th>Amount</th>
                <th>Description</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span className="badge badge-success">Earned</span></td>
                <td style={{ color: 'var(--secondary-color)' }}>+50</td>
                <td>Completed inference task #1234</td>
                <td>{new Date().toLocaleDateString()}</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">Earned</span></td>
                <td style={{ color: 'var(--secondary-color)' }}>+100</td>
                <td>GPU compute contribution</td>
                <td>{new Date(Date.now() - 86400000).toLocaleDateString()}</td>
              </tr>
              <tr>
                <td><span className="badge badge-warning">Spent</span></td>
                <td style={{ color: 'var(--danger-color)' }}>-30</td>
                <td>Task submission fee</td>
                <td>{new Date(Date.now() - 172800000).toLocaleDateString()}</td>
              </tr>
              <tr>
                <td><span className="badge badge-success">Earned</span></td>
                <td style={{ color: 'var(--secondary-color)' }}>+30</td>
                <td>Node uptime bonus</td>
                <td>{new Date(Date.now() - 259200000).toLocaleDateString()}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Credits;
