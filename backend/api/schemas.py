"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Node Schemas
class NodeRegister(BaseModel):
    """Schema for node registration."""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    cpu_cores: int = Field(default=0, ge=0)
    memory_total: float = Field(default=0.0, ge=0.0)
    gpu_enabled: bool = False
    gpu_memory: float = Field(default=0.0, ge=0.0)
    ip_address: Optional[str] = None
    port: Optional[int] = None


class NodeUpdate(BaseModel):
    """Schema for node status update (heartbeat)."""
    cpu_available: Optional[int] = None
    memory_available: Optional[float] = None
    status: Optional[str] = None


class NodeResponse(BaseModel):
    """Schema for node response."""
    id: str
    name: str
    status: str
    cpu_cores: int
    cpu_available: int
    memory_total: float
    memory_available: float
    gpu_enabled: bool
    gpu_memory: float
    last_heartbeat: Optional[datetime]
    registered_at: Optional[datetime]
    ip_address: Optional[str]
    port: Optional[int]

    class Config:
        from_attributes = True


# Task Schemas
class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    type: str = Field(..., min_length=1, max_length=50)
    input_data: Dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0, ge=-10, le=10)
    credits_reward: int = Field(default=10, ge=1)


class TaskResult(BaseModel):
    """Schema for submitting task result."""
    result: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str
    type: str
    status: str
    priority: int
    input_data: Optional[Dict[str, Any]]
    result: Optional[Dict[str, Any]]
    error_message: Optional[str]
    node_id: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    credits_reward: int

    class Config:
        from_attributes = True


# Credit Schemas
class CreditTransaction(BaseModel):
    """Schema for credit transaction."""
    node_id: str
    amount: int
    transaction_type: str
    description: Optional[str] = None
    task_id: Optional[str] = None


class CreditBalance(BaseModel):
    """Schema for credit balance response."""
    node_id: str
    total_balance: int
    transactions: List[CreditTransaction] = []


# Resource Schema
class ResourceInfo(BaseModel):
    """Schema for resource information."""
    cpu_cores: int
    cpu_percent: float
    cpu_available: int
    memory_total: float
    memory_used: float
    memory_available: float
    memory_percent: float
    gpu_enabled: bool
    gpu_memory_total: float
    gpu_memory_used: float
    gpu_memory_available: float


# P2P Schema
class PeerOffer(BaseModel):
    """Schema for WebRTC offer."""
    offer: Dict[str, Any]
    node_id: str


class PeerAnswer(BaseModel):
    """Schema for WebRTC answer."""
    answer: Dict[str, Any]
    node_id: str


# Generic Response
class ApiResponse(BaseModel):
    """Generic API response wrapper."""
    success: bool
    message: str
    data: Optional[Any] = None
