# EdgeAGI - Decentralized AI Swarm Orchestrator

## Overview

EdgeAGI is an open-source decentralized AI swarm orchestrator that enables users to:
- Install a lightweight app and opt-in to share idle CPU/GPU resources
- Join a peer-to-peer compute network
- Run small AI tasks locally or across devices
- Earn rewards/credits for contributing compute resources

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Node A        │     │   Node B        │     │   Coordinator   │
│  (Dashboard)    │◄───►│  (Worker)       │◄───►│  (Server)       │
│                 │     │                 │     │                 │
│ - Resource Pool │     │ - Task Runner   │     │ - Task Queue    │
│ - Status UI     │     │ - Model Infer.  │     │ - Node Registry │
│ - Credit Ledger │     │ - Heartbeat     │     │ - Reward System │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Tech Stack

- **Backend**: Python FastAPI (async, high-performance)
- **Frontend**: React + Vite + TypeScript
- **P2P Communication**: WebRTC (via simple-peer abstraction)
- **Task Queue**: In-memory with Redis option
- **Database**: SQLite (default) / PostgreSQL (production)
- **AI Runtime**: ONNX Runtime / Transformers (small models)

## Quick Start

### Option 1: Docker (Recommended)

The easiest way to run EdgeAGI is with Docker Compose.

#### Prerequisites

- Docker Desktop installed (for Mac M2, ensure you have the ARM version)
- Docker Compose (included with Docker Desktop)

#### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd edgeagi
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

#### Docker Commands

```bash
# Start in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up --build

# Clean up everything
docker-compose down -v
```

### Option 2: Local Development

#### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Access the Dashboard

Open http://localhost:5173 in your browser.

## Project Structure

```
edgeagi/
├── backend/
│   ├── api/              # API endpoints
│   ├── routes/           # Route definitions
│   ├── services/         # Business logic
│   ├── models/           # Data models
│   ├── utils/            # Utilities
│   ├── tests/            # Test suite
│   ├── main.py           # FastAPI app entry
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API services
│   │   └── styles/       # CSS styles
│   ├── public/           # Static assets
│   └── package.json
├── docs/                 # Documentation
└── README.md
```

## Core Features

### 1. Node Registration & Heartbeat
Nodes register with the coordinator and send periodic heartbeats to indicate availability.

### 2. Resource Detection
Automatic detection of available CPU cores, GPU memory, and RAM.

### 3. Task Distribution
Tasks are queued and distributed to available nodes based on resource requirements.

### 4. Local AI Inference
Support for running small AI models (text classification, image recognition) locally.

### 5. Reward System
Nodes earn credits for completed tasks. Credits are tracked in a simple ledger.

### 6. P2P Communication
WebRTC-based direct communication between nodes for task offloading.

## Configuration

See `.env.example` for available configuration options.

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./edgeagi.db |
| REDIS_URL | Redis connection (optional) | None |
| SECRET_KEY | JWT secret key | auto-generated |
| NODE_ID | Unique node identifier | auto-generated |
| API_HOST | Backend host | 0.0.0.0 |
| API_PORT | Backend port | 8000 |

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/nodes/register | Register a new node |
| GET | /api/nodes | List all nodes |
| POST | /api/nodes/{id}/heartbeat | Send heartbeat |
| POST | /api/tasks | Submit a task |
| GET | /api/tasks | List tasks |
| GET | /api/tasks/{id} | Get task status |
| POST | /api/tasks/{id}/result | Submit task result |
| GET | /api/credits | Get credit balance |
| GET | /api/resources | Get available resources |

## Security

- Environment variables for sensitive data
- Input validation on all endpoints
- CORS configuration for frontend
- Rate limiting on API endpoints
- JWT authentication (optional)

## Extending

### Adding New Task Types
1. Define task schema in `backend/models/task.py`
2. Implement handler in `backend/services/task_handler.py`
3. Add UI component in `frontend/src/components/tasks/`

### Integrating Blockchain Rewards
1. Implement `backend/services/reward_service.py` with blockchain provider
2. Add wallet management in `backend/models/wallet.py`
3. Update frontend credit display

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Roadmap

- [x] MVP: Basic node registration and task queue
- [x] MVP: Dashboard UI
- [x] MVP: Local AI inference demo
- [ ] P2P WebRTC mesh network
- [ ] Blockchain reward integration
- [ ] Advanced task scheduling
- [ ] Multi-model support
- [ ] Mobile app
