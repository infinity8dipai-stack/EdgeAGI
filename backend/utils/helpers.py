"""
Utility functions for EdgeAGI.
"""
import psutil
import platform
from typing import Dict, Any


def get_system_resources() -> Dict[str, Any]:
    """Get current system resource information."""
    # CPU info
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_cores = psutil.cpu_count(logical=True)
    cpu_physical = psutil.cpu_count(logical=False) or cpu_cores
    
    # Memory info
    memory = psutil.virtual_memory()
    memory_total_gb = memory.total / (1024 ** 3)
    memory_available_gb = memory.available / (1024 ** 3)
    memory_used_gb = memory.used / (1024 ** 3)
    memory_percent = memory.percent
    
    # GPU info (basic detection)
    gpu_enabled = False
    gpu_memory_total = 0.0
    gpu_memory_used = 0.0
    gpu_memory_available = 0.0
    
    try:
        import subprocess
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total,memory.used", "--format=csv,nounits"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            if lines:
                gpu_enabled = True
                total, used = map(float, lines[0].split(', '))
                gpu_memory_total = total / 1024  # Convert to GB
                gpu_memory_used = used / 1024
                gpu_memory_available = gpu_memory_total - gpu_memory_used
    except Exception:
        pass  # No GPU or nvidia-smi not available
    
    return {
        "cpu_cores": cpu_cores,
        "cpu_physical": cpu_physical,
        "cpu_percent": cpu_percent,
        "cpu_available": int(cpu_cores * (100 - cpu_percent) / 100),
        "memory_total": round(memory_total_gb, 2),
        "memory_used": round(memory_used_gb, 2),
        "memory_available": round(memory_available_gb, 2),
        "memory_percent": memory_percent,
        "gpu_enabled": gpu_enabled,
        "gpu_memory_total": round(gpu_memory_total, 2),
        "gpu_memory_used": round(gpu_memory_used, 2),
        "gpu_memory_available": round(gpu_memory_available, 2),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version()
    }


def is_resource_available(max_cpu: float = 80.0, max_memory: float = 80.0) -> bool:
    """Check if system resources are available within thresholds."""
    resources = get_system_resources()
    
    cpu_ok = resources["cpu_percent"] < max_cpu
    memory_ok = resources["memory_percent"] < max_memory
    
    return cpu_ok and memory_ok


def generate_node_id(prefix: str = "node") -> str:
    """Generate a unique node ID."""
    import uuid
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes_value) < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"
