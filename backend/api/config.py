"""
EdgeAGI Configuration Module
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import uuid


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "sqlite:///./edgeagi.db"
    
    # Redis
    redis_url: Optional[str] = None
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Node Configuration
    node_id: str = f"node-{uuid.uuid4().hex[:8]}"
    node_name: str = "EdgeAGI-Node"
    heartbeat_interval: int = 30
    
    # Resource Limits
    max_cpu_percent: float = 80.0
    max_memory_percent: float = 80.0
    gpu_enabled: bool = False
    
    # Rewards
    credits_per_task: int = 10
    reward_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "edgeagi.log"
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # P2P Settings
    p2p_enabled: bool = True
    webrtc_ice_servers: List[str] = ["stun:stun.l.google.com:19302"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
