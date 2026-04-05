"""
Service for managing nodes in the swarm network.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from models.database import Node
from api.schemas import NodeRegister, NodeUpdate


class NodeService:
    """Service for node management operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def register_node(self, node_data: NodeRegister) -> Node:
        """Register a new node in the network."""
        node_id = node_data.id or f"node-{uuid.uuid4().hex[:12]}"
        
        # Check if node already exists
        existing = self.get_node(node_id)
        if existing:
            # Update existing node
            existing.name = node_data.name
            existing.cpu_cores = node_data.cpu_cores
            existing.memory_total = node_data.memory_total
            existing.gpu_enabled = node_data.gpu_enabled
            existing.gpu_memory = node_data.gpu_memory
            existing.ip_address = node_data.ip_address
            existing.port = node_data.port
            existing.status = "online"
            existing.last_heartbeat = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # Create new node
        node = Node(
            id=node_id,
            name=node_data.name,
            cpu_cores=node_data.cpu_cores,
            memory_total=node_data.memory_total,
            gpu_enabled=node_data.gpu_enabled,
            gpu_memory=node_data.gpu_memory,
            ip_address=node_data.ip_address,
            port=node_data.port,
            status="online",
            last_heartbeat=datetime.utcnow(),
            registered_at=datetime.utcnow()
        )
        
        self.db.add(node)
        self.db.commit()
        self.db.refresh(node)
        return node
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.db.query(Node).filter(Node.id == node_id).first()
    
    def list_nodes(self, status: Optional[str] = None) -> List[Node]:
        """List all nodes, optionally filtered by status."""
        query = select(Node)
        if status:
            query = query.where(Node.status == status)
        result = self.db.execute(query)
        return list(result.scalars().all())
    
    def update_heartbeat(self, node_id: str, update: NodeUpdate) -> Optional[Node]:
        """Update node heartbeat and status."""
        node = self.get_node(node_id)
        if not node:
            return None
        
        node.last_heartbeat = datetime.utcnow()
        
        if update.cpu_available is not None:
            node.cpu_available = update.cpu_available
        if update.memory_available is not None:
            node.memory_available = update.memory_available
        if update.status is not None:
            node.status = update.status
        
        self.db.commit()
        self.db.refresh(node)
        return node
    
    def set_node_status(self, node_id: str, status: str) -> Optional[Node]:
        """Set node status (online, offline, busy)."""
        node = self.get_node(node_id)
        if not node:
            return None
        
        node.status = status
        if status == "offline":
            node.cpu_available = 0
            node.memory_available = 0
        
        self.db.commit()
        self.db.refresh(node)
        return node
    
    def get_online_nodes(self) -> List[Node]:
        """Get all online nodes."""
        return self.list_nodes(status="online")
    
    def get_available_nodes(self) -> List[Node]:
        """Get nodes that are available for tasks."""
        now = datetime.utcnow()
        threshold = now - timedelta(seconds=60)  # Considered offline if no heartbeat in 60s
        
        nodes = self.get_online_nodes()
        available = []
        
        for node in nodes:
            if (node.last_heartbeat and 
                node.last_heartbeat > threshold and 
                node.status == "online"):
                available.append(node)
        
        return available
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the network."""
        node = self.get_node(node_id)
        if not node:
            return False
        
        self.db.delete(node)
        self.db.commit()
        return True
    
    def mark_offline_stale_nodes(self) -> int:
        """Mark nodes as offline if they haven't sent heartbeat recently."""
        threshold = datetime.utcnow() - timedelta(seconds=60)
        
        stale_nodes = self.db.query(Node).filter(
            Node.status == "online",
            Node.last_heartbeat < threshold
        ).all()
        
        count = 0
        for node in stale_nodes:
            node.status = "offline"
            count += 1
        
        if count > 0:
            self.db.commit()
        
        return count
