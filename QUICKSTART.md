# EdgeAGI Quick Start Guide for Mac M2

## Running with Docker (Recommended)

### Step 1: Install Docker Desktop

1. Download Docker Desktop for Mac from https://www.docker.com/products/docker-desktop/
2. Choose the version for Apple Silicon (M1/M2)
3. Install and launch Docker Desktop
4. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

### Step 2: Clone and Setup

```bash
# Navigate to the project directory
cd /workspace/edgeagi

# Copy environment file
cp .env.example .env
```

### Step 3: Build and Run

```bash
# Build and start all services
docker-compose up --build
```

Wait for the build to complete (first time may take 5-10 minutes).

### Step 4: Access the Application

Open your browser and go to:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Common Commands

```bash
# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Clean up everything (including database)
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If you get a port conflict error:
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Stop the conflicting process or change ports in docker-compose.yml
```

### Docker Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Frontend Can't Connect to Backend

Make sure the API URL is correct in `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

## Testing the MVP

1. **Register a Node**: Go to Nodes page and register a new node
2. **Create a Task**: Go to Tasks page and create an AI task
3. **View Dashboard**: Check the main dashboard for stats
4. **Check Credits**: View the credits ledger

## Next Steps

- Review the full README.md for detailed documentation
- Check the API documentation at http://localhost:8000/docs
- Explore the source code in `backend/` and `frontend/`
- Read about extending EdgeAGI in the docs/ folder
