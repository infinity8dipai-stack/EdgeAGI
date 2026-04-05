"""
Service for managing tasks in the swarm network.
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid

from models.database import Task, Node
from api.schemas import TaskCreate, TaskResult


class TaskService:
    """Service for task management operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task_id = f"task-{uuid.uuid4().hex[:12]}"
        
        task = Task(
            id=task_id,
            type=task_data.type,
            status="pending",
            priority=task_data.priority,
            input_data=task_data.input_data,
            credits_reward=task_data.credits_reward,
            created_at=datetime.utcnow()
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def list_tasks(
        self, 
        status: Optional[str] = None,
        node_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks with optional filters."""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if node_id:
            query = query.filter(Task.node_id == node_id)
        
        query = query.order_by(Task.priority.desc(), Task.created_at.desc())
        return query.limit(limit).all()
    
    def assign_task(self, task_id: str, node_id: str) -> Optional[Task]:
        """Assign a task to a node."""
        task = self.get_task(task_id)
        if not task or task.status != "pending":
            return None
        
        task.node_id = node_id
        task.status = "running"
        task.started_at = datetime.utcnow()
        
        # Update node status to busy
        node = self.db.query(Node).filter(Node.id == node_id).first()
        if node:
            node.status = "busy"
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def complete_task(
        self, 
        task_id: str, 
        result: Dict[str, Any],
        error_message: Optional[str] = None
    ) -> Optional[Task]:
        """Mark a task as completed."""
        task = self.get_task(task_id)
        if not task:
            return None
        
        task.status = "failed" if error_message else "completed"
        task.result = result
        task.error_message = error_message
        task.completed_at = datetime.utcnow()
        
        # Update node status back to online
        if task.node_id:
            node = self.db.query(Node).filter(Node.id == task.node_id).first()
            if node:
                node.status = "online"
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def fail_task(self, task_id: str, error_message: str) -> Optional[Task]:
        """Mark a task as failed."""
        return self.complete_task(task_id, {}, error_message)
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks ordered by priority."""
        return (
            self.db.query(Task)
            .filter(Task.status == "pending")
            .order_by(Task.priority.desc(), Task.created_at.asc())
            .all()
        )
    
    def get_running_tasks(self) -> List[Task]:
        """Get all running tasks."""
        return (
            self.db.query(Task)
            .filter(Task.status == "running")
            .all()
        )
    
    def cancel_task(self, task_id: str) -> Optional[Task]:
        """Cancel a pending or running task."""
        task = self.get_task(task_id)
        if not task or task.status in ["completed", "failed"]:
            return None
        
        task.status = "cancelled"
        task.completed_at = datetime.utcnow()
        
        # Update node status if task was running
        if task.node_id:
            node = self.db.query(Node).filter(Node.id == task.node_id).first()
            if node:
                node.status = "online"
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def get_next_available_task(self, node_id: str) -> Optional[Task]:
        """Get the next available task for a node."""
        pending_tasks = self.get_pending_tasks()
        
        if not pending_tasks:
            return None
        
        # Return highest priority task
        return pending_tasks[0]
