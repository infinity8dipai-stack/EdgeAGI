import React, { useState, useEffect } from 'react';
import { getNodes, getTasks, getResources, createTask } from '../services/api';

interface DashboardStats {
  totalNodes: number;
  onlineNodes: number;
  pendingTasks: number;
  completedTasks: number;
  totalCredits: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalNodes: 0,
    onlineNodes: 0,
    pendingTasks: 0,
    completedTasks: 0,
    totalCredits: 0,
  });
  const [resources, setResources] = useState<any>(null);
  const [recentTasks, setRecentTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const [nodesRes, tasksRes, resourcesRes] = await Promise.all([
        getNodes(),
        getTasks(),
        getResources(),
      ]);

      const nodes = nodesRes.data;
      const tasks = tasksRes.data;

      setStats({
        totalNodes: nodes.length,
        onlineNodes: nodes.filter((n: any) => n.status === 'online').length,
        pendingTasks: tasks.filter((t: any) => t.status === 'pending').length,
        completedTasks: tasks.filter((t: any) => t.status === 'completed').length,
        totalCredits: 0,
      });

      setResources(resourcesRes.data);
      setRecentTasks(tasks.slice(0, 5));
      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Nodes</h3>
          <p className="stat-value">{stats.totalNodes}</p>
          <span className="stat-sub">{stats.onlineNodes} online</span>
        </div>
        <div className="stat-card">
          <h3>Pending Tasks</h3>
          <p className="stat-value">{stats.pendingTasks}</p>
          <span className="stat-sub">Waiting to be processed</span>
        </div>
        <div className="stat-card">
          <h3>Completed Tasks</h3>
          <p className="stat-value">{stats.completedTasks}</p>
          <span className="stat-sub">Successfully executed</span>
        </div>
        <div className="stat-card">
          <h3>System Resources</h3>
          <p className="stat-value">
            {resources ? `${resources.cpu_percent.toFixed(1)}% CPU` : '-'}
          </p>
          <span className="stat-sub">
            {resources ? `${resources.memory_percent.toFixed(1)}% Memory` : ''}
          </span>
        </div>
      </div>

      <div className="dashboard-sections">
        <section className="section">
          <h2>Resource Overview</h2>
          {resources && (
            <div className="resource-details">
              <div className="resource-item">
                <label>CPU Cores:</label>
                <span>{resources.cpu_cores} available</span>
              </div>
              <div className="resource-item">
                <label>Memory:</label>
                <span>{resources.memory_available} GB / {resources.memory_total} GB</span>
              </div>
              <div className="resource-item">
                <label>GPU:</label>
                <span>{resources.gpu_enabled ? 'Enabled' : 'Not available'}</span>
              </div>
            </div>
          )}
        </section>

        <section className="section">
          <h2>Recent Tasks</h2>
          {recentTasks.length > 0 ? (
            <table className="task-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {recentTasks.map((task) => (
                  <tr key={task.id}>
                    <td className="task-id">{task.id.slice(0, 12)}...</td>
                    <td>{task.type}</td>
                    <td>
                      <span className={`status-badge ${task.status}`}>
                        {task.status}
                      </span>
                    </td>
                    <td>{new Date(task.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="empty-state">No tasks yet. Create one to get started!</p>
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
