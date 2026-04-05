import React, { useState, useEffect } from 'react';
import { getNodes, sendHeartbeat } from '../services/api';

interface Node {
  id: string;
  name: string;
  status: string;
  cpu_cores: number;
  memory_total: number;
  cpu_available: number;
  memory_available: number;
  last_heartbeat: string;
}

const Nodes: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [loading, setLoading] = useState(true);
  const [newNodeName, setNewNodeName] = useState('');

  useEffect(() => {
    loadNodes();
    const interval = setInterval(loadNodes, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadNodes = async () => {
    try {
      const response = await getNodes();
      setNodes(response.data);
    } catch (error) {
      console.error('Failed to load nodes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterNode = async (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would call an API to register
    alert('Node registration would be implemented here');
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
        <h2>Nodes</h2>
        <p>Manage and monitor connected compute nodes</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Register New Node</h3>
        </div>
        <form onSubmit={handleRegisterNode}>
          <div className="form-group">
            <label>Node Name</label>
            <input
              type="text"
              className="form-input"
              value={newNodeName}
              onChange={(e) => setNewNodeName(e.target.value)}
              placeholder="Enter node name"
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Register Node
          </button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Connected Nodes ({nodes.length})</h3>
        </div>
        {nodes.length === 0 ? (
          <div className="empty-state">
            <h3>No nodes connected</h3>
            <p>Register a node to get started</p>
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Status</th>
                  <th>CPU</th>
                  <th>Memory</th>
                  <th>Last Heartbeat</th>
                </tr>
              </thead>
              <tbody>
                {nodes.map((node) => (
                  <tr key={node.id}>
                    <td>{node.name}</td>
                    <td>
                      <span className={`badge ${node.status === 'online' ? 'badge-success' : 'badge-warning'}`}>
                        {node.status}
                      </span>
                    </td>
                    <td>
                      {node.cpu_available}/{node.cpu_cores} cores
                      <div className="resource-bar">
                        <div 
                          className="resource-bar-fill" 
                          style={{ width: `${(node.cpu_available / node.cpu_cores) * 100}%` }}
                        ></div>
                      </div>
                    </td>
                    <td>
                      {Math.round(node.memory_available / 1024)}GB / {Math.round(node.memory_total / 1024)}GB
                      <div className="resource-bar">
                        <div 
                          className="resource-bar-fill" 
                          style={{ width: `${(node.memory_available / node.memory_total) * 100}%` }}
                        ></div>
                      </div>
                    </td>
                    <td>{new Date(node.last_heartbeat).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Nodes;
