"""
API Routes for EdgeAGI
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from api.database import get_db
from api.schemas import (
    NodeRegister, NodeResponse, NodeUpdate,
    TaskCreate, TaskResponse, TaskResult,
    CreditBalance, ResourceInfo, ApiResponse
)
from services.node_service import NodeService
from services.task_service import TaskService
from services.reward_service import RewardService
from services.ai_service import get_ai_service
from utils.helpers import get_system_resources

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/nodes/register", response_model=NodeResponse, tags=["Nodes"])
async def register_node(
    node_data: NodeRegister,
    db: Session = Depends(get_db)
):
    """Register a new node in the swarm network."""
    service = NodeService(db)
    node = service.register_node(node_data)
    
    # Give signup bonus
    reward_service = RewardService(db)
    reward_service.give_signup_bonus(node.id)
    
    logger.info(f"Node registered: {node.id}")
    return node


@router.get("/nodes", response_model=List[NodeResponse], tags=["Nodes"])
async def list_nodes(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all nodes, optionally filtered by status."""
    service = NodeService(db)
    return service.list_nodes(status)


@router.get("/nodes/{node_id}", response_model=NodeResponse, tags=["Nodes"])
async def get_node(
    node_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific node by ID."""
    service = NodeService(db)
    node = service.get_node(node_id)
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return node


@router.post("/nodes/{node_id}/heartbeat", response_model=NodeResponse, tags=["Nodes"])
async def send_heartbeat(
    node_id: str,
    update: NodeUpdate,
    db: Session = Depends(get_db)
):
    """Send heartbeat to update node status."""
    service = NodeService(db)
    node = service.update_heartbeat(node_id, update)
    
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    return node


@router.delete("/nodes/{node_id}", tags=["Nodes"])
async def remove_node(
    node_id: str,
    db: Session = Depends(get_db)
):
    """Remove a node from the network."""
    service = NodeService(db)
    
    if not service.remove_node(node_id):
        raise HTTPException(status_code=404, detail="Node not found")
    
    return {"success": True, "message": f"Node {node_id} removed"}


@router.post("/tasks", response_model=TaskResponse, tags=["Tasks"])
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Create a new AI task."""
    service = TaskService(db)
    task = service.create_task(task_data)
    
    logger.info(f"Task created: {task.id}, type: {task.type}")
    
    # Try to assign to available node immediately
    node_service = NodeService(db)
    available_nodes = node_service.get_available_nodes()
    
    if available_nodes:
        # Assign to first available node
        node = available_nodes[0]
        service.assign_task(task.id, node.id)
        logger.info(f"Task {task.id} assigned to node {node.id}")
    
    return task


@router.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(
    status: Optional[str] = None,
    node_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List tasks with optional filters."""
    service = TaskService(db)
    return service.list_tasks(status, node_id, limit)


@router.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific task by ID."""
    service = TaskService(db)
    task = service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.post("/tasks/{task_id}/result", response_model=TaskResponse, tags=["Tasks"])
async def submit_task_result(
    task_id: str,
    result_data: TaskResult,
    db: Session = Depends(get_db)
):
    """Submit result for a running task."""
    task_service = TaskService(db)
    task = task_service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    completed_task = task_service.complete_task(
        task_id, 
        result_data.result,
        result_data.error_message
    )
    
    # Reward node for completion
    if completed_task and completed_task.status == "completed" and task.node_id:
        reward_service = RewardService(db)
        reward_service.reward_task_completion(
            task.node_id,
            task_id,
            task.credits_reward
        )
        logger.info(f"Task {task_id} completed, rewarded {task.credits_reward} credits")
    
    return completed_task


@router.delete("/tasks/{task_id}", tags=["Tasks"])
async def cancel_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Cancel a pending or running task."""
    service = TaskService(db)
    task = service.cancel_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or cannot be cancelled")
    
    return {"success": True, "message": f"Task {task_id} cancelled"}


@router.get("/credits/{node_id}", response_model=CreditBalance, tags=["Credits"])
async def get_credits(
    node_id: str,
    db: Session = Depends(get_db)
):
    """Get credit balance for a node."""
    reward_service = RewardService(db)
    
    # Verify node exists
    node_service = NodeService(db)
    node = node_service.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    balance = reward_service.get_node_balance(node_id)
    transactions = reward_service.get_transactions(node_id, limit=20)
    
    return CreditBalance(
        node_id=node_id,
        total_balance=balance,
        transactions=[t.to_dict() for t in transactions]
    )


@router.get("/resources", response_model=ResourceInfo, tags=["System"])
async def get_resources():
    """Get current system resource information."""
    resources = get_system_resources()
    return ResourceInfo(**resources)


@router.post("/tasks/execute_local", response_model=dict, tags=["Tasks"])
async def execute_local_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """Execute a task locally and return result immediately."""
    ai_service = get_ai_service()
    
    result = await ai_service.run_task(task_data.type, task_data.input_data)
    
    return {
        "success": result.get("success", False),
        "result": result,
        "credits_that_would_be_earned": task_data.credits_reward
    }


@router.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "EdgeAGI Coordinator"}
