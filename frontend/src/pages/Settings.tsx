import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [settings, setSettings] = useState({
    nodeName: 'My Node',
    autoStart: true,
    gpuEnabled: false,
    maxCpuUsage: 80,
    maxMemoryUsage: 75,
    p2pEnabled: true,
    notificationsEnabled: true,
  });

  const handleChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    alert('Settings saved! (This is a demo - settings would be persisted in production)');
  };

  return (
    <div>
      <div className="page-header">
        <h2>Settings</h2>
        <p>Configure your node and application preferences</p>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Node Configuration</h3>
        </div>
        <div className="form-group">
          <label>Node Name</label>
          <input
            type="text"
            className="form-input"
            value={settings.nodeName}
            onChange={(e) => handleChange('nodeName', e.target.value)}
            placeholder="Enter node name"
          />
        </div>
        <div className="form-group">
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={settings.autoStart}
              onChange={(e) => handleChange('autoStart', e.target.checked)}
              style={{ width: 'auto' }}
            />
            Auto-start node on application launch
          </label>
        </div>
        <div className="form-group">
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={settings.gpuEnabled}
              onChange={(e) => handleChange('gpuEnabled', e.target.checked)}
              style={{ width: 'auto' }}
            />
            Enable GPU acceleration (if available)
          </label>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Resource Limits</h3>
        </div>
        <div className="form-group">
          <label>Max CPU Usage (%)</label>
          <input
            type="range"
            min="0"
            max="100"
            value={settings.maxCpuUsage}
            onChange={(e) => handleChange('maxCpuUsage', Number(e.target.value))}
            style={{ width: '100%' }}
          />
          <div style={{ textAlign: 'right', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            {settings.maxCpuUsage}%
          </div>
        </div>
        <div className="form-group">
          <label>Max Memory Usage (%)</label>
          <input
            type="range"
            min="0"
            max="100"
            value={settings.maxMemoryUsage}
            onChange={(e) => handleChange('maxMemoryUsage', Number(e.target.value))}
            style={{ width: '100%' }}
          />
          <div style={{ textAlign: 'right', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            {settings.maxMemoryUsage}%
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Network Settings</h3>
        </div>
        <div className="form-group">
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={settings.p2pEnabled}
              onChange={(e) => handleChange('p2pEnabled', e.target.checked)}
              style={{ width: 'auto' }}
            />
            Enable Peer-to-Peer communication
          </label>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Allow direct connections with other nodes in the swarm for faster task distribution.
          </p>
        </div>
        <div className="form-group">
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={settings.notificationsEnabled}
              onChange={(e) => handleChange('notificationsEnabled', e.target.checked)}
              style={{ width: 'auto' }}
            />
            Enable desktop notifications
          </label>
        </div>
      </div>

      <button onClick={handleSave} className="btn btn-primary">
        Save Settings
      </button>
    </div>
  );
};

export default Settings;
