"""
Database Models for EdgeAGI
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Node(Base):
    """Represents a compute node in the swarm network."""
    
    __tablename__ = "nodes"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="offline")  # online, offline, busy
    cpu_cores = Column(Integer, default=0)
    cpu_available = Column(Integer, default=0)
    memory_total = Column(Float, default=0.0)  # in GB
    memory_available = Column(Float, default=0.0)  # in GB
    gpu_enabled = Column(Boolean, default=False)
    gpu_memory = Column(Float, default=0.0)  # in GB
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    registered_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    
    # Relationships
    tasks = relationship("Task", back_populates="node")
    credits = relationship("CreditLedger", back_populates="node")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "cpu_cores": self.cpu_cores,
            "cpu_available": self.cpu_available,
            "memory_total": self.memory_total,
            "memory_available": self.memory_available,
            "gpu_enabled": self.gpu_enabled,
            "gpu_memory": self.gpu_memory,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
            "ip_address": self.ip_address,
            "port": self.port,
        }


class Task(Base):
    """Represents an AI task to be executed."""
    
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)  # text_classification, image_recognition, etc.
    status = Column(String, default="pending")  # pending, running, completed, failed
    priority = Column(Integer, default=0)
    input_data = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    node_id = Column(String, ForeignKey("nodes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    credits_reward = Column(Integer, default=10)
    
    # Relationships
    node = relationship("Node", back_populates="tasks")
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "input_data": self.input_data,
            "result": self.result,
            "error_message": self.error_message,
            "node_id": self.node_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "credits_reward": self.credits_reward,
        }


class CreditLedger(Base):
    """Tracks credits earned by nodes for completed tasks."""
    
    __tablename__ = "credit_ledger"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)  # earn, spend, bonus
    description = Column(String, nullable=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    node = relationship("Node", back_populates="credits")
    task = relationship("Task")
    
    def to_dict(self):
        return {
            "id": self.id,
            "node_id": self.node_id,
            "amount": self.amount,
            "balance_after": self.balance_after,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "task_id": self.task_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PeerConnection(Base):
    """Tracks P2P connections between nodes."""
    
    __tablename__ = "peer_connections"
    
    id = Column(String, primary_key=True)
    node_a_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    node_b_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    status = Column(String, default="connecting")  # connecting, connected, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "node_a_id": self.node_a_id,
            "node_b_id": self.node_b_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
