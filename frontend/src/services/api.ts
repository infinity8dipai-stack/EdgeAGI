import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Node endpoints
export const registerNode = (data: { name: string; cpu_cores: number; memory_total: number; gpu_enabled?: boolean }) =>
  api.post('/nodes/register', data);

export const getNodes = (status?: string) =>
  api.get('/nodes', { params: { status } });

export const getNode = (nodeId: string) =>
  api.get(`/nodes/${nodeId}`);

export const sendHeartbeat = (nodeId: string, data: { cpu_available?: number; memory_available?: number; status?: string }) =>
  api.post(`/nodes/${nodeId}/heartbeat`, data);

// Task endpoints
export const createTask = (data: { type: string; input_data: Record<string, any>; priority?: number; credits_reward?: number }) =>
  api.post('/tasks', data);

export const getTasks = (status?: string, nodeId?: string) =>
  api.get('/tasks', { params: { status, node_id: nodeId } });

export const getTask = (taskId: string) =>
  api.get(`/tasks/${taskId}`);

export const submitTaskResult = (taskId: string, result: Record<string, any>, error_message?: string) =>
  api.post(`/tasks/${taskId}/result`, { result, error_message });

export const executeLocalTask = (data: { type: string; input_data: Record<string, any>; credits_reward?: number }) =>
  api.post('/tasks/execute_local', data);

// Credits endpoints
export const getCredits = (nodeId: string) =>
  api.get(`/credits/${nodeId}`);

// System endpoints
export const getResources = () =>
  api.get('/resources');

export const healthCheck = () =>
  api.get('/');

export default api;
