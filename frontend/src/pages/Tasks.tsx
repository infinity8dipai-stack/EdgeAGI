import React, { useState, useEffect } from 'react';
import { getTasks, createTask } from '../services/api';

interface Task {
  id: string;
  type: string;
  status: string;
  priority: number;
  created_at: string;
  node_id?: string;
}

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [taskType, setTaskType] = useState('inference');
  const [priority, setPriority] = useState(1);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await getTasks();
      setTasks(response.data);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createTask({
        type: taskType,
        input_data: { sample: 'data' },
        priority: priority,
        credits_reward: 10
      });
      loadTasks();
      alert('Task created successfully!');
    } catch (error) {
      console.error('Failed to create task:', error);
      alert('Failed to create task');
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
        <h2>Tasks</h2>
        <p>Create and monitor AI tasks across the swarm</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Create New Task</h3>
        </div>
        <form onSubmit={handleCreateTask}>
          <div className="form-group">
            <label>Task Type</label>
            <select
              className="form-input"
              value={taskType}
              onChange={(e) => setTaskType(e.target.value)}
            >
              <option value="inference">AI Inference</option>
              <option value="training">Model Training</option>
              <option value="preprocessing">Data Preprocessing</option>
              <option value="custom">Custom Task</option>
            </select>
          </div>
          <div className="form-group">
            <label>Priority</label>
            <select
              className="form-input"
              value={priority}
              onChange={(e) => setPriority(Number(e.target.value))}
            >
              <option value={1}>Low</option>
              <option value={5}>Normal</option>
              <option value={10}>High</option>
            </select>
          </div>
          <button type="submit" className="btn btn-primary">
            Create Task
          </button>
        </form>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Task Queue ({tasks.length})</h3>
        </div>
        {tasks.length === 0 ? (
          <div className="empty-state">
            <h3>No tasks in queue</h3>
            <p>Create a task to get started</p>
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Priority</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <tr key={task.id}>
                    <td><code>{task.id.slice(0, 8)}...</code></td>
                    <td>{task.type}</td>
                    <td>
                      <span className={`badge 
                        ${task.status === 'completed' ? 'badge-success' : 
                          task.status === 'pending' ? 'badge-warning' : 
                          task.status === 'failed' ? 'badge-danger' : 'badge-info'}`}>
                        {task.status}
                      </span>
                    </td>
                    <td>{task.priority}</td>
                    <td>{new Date(task.created_at).toLocaleString()}</td>
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

export default Tasks;
