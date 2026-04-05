"""
Service for managing credits and rewards.
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import uuid

from models.database import CreditLedger, Node


class RewardService:
    """Service for credit and reward management."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_node_balance(self, node_id: str) -> int:
        """Get total credit balance for a node."""
        transactions = (
            self.db.query(CreditLedger)
            .filter(CreditLedger.node_id == node_id)
            .all()
        )
        
        return sum(t.amount for t in transactions)
    
    def add_credits(
        self, 
        node_id: str, 
        amount: int, 
        description: str,
        task_id: Optional[str] = None,
        transaction_type: str = "earn"
    ) -> CreditLedger:
        """Add credits to a node's balance."""
        current_balance = self.get_node_balance(node_id)
        new_balance = current_balance + amount
        
        transaction = CreditLedger(
            node_id=node_id,
            amount=amount,
            balance_after=new_balance,
            transaction_type=transaction_type,
            description=description,
            task_id=task_id,
            created_at=datetime.utcnow()
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def spend_credits(
        self,
        node_id: str,
        amount: int,
        description: str,
        transaction_type: str = "spend"
    ) -> Optional[CreditLedger]:
        """Spend credits from a node's balance."""
        current_balance = self.get_node_balance(node_id)
        
        if current_balance < amount:
            return None
        
        new_balance = current_balance - amount
        
        transaction = CreditLedger(
            node_id=node_id,
            amount=-amount,  # Negative for spending
            balance_after=new_balance,
            transaction_type=transaction_type,
            description=description,
            created_at=datetime.utcnow()
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_transactions(
        self, 
        node_id: str, 
        limit: int = 50
    ) -> List[CreditLedger]:
        """Get recent transactions for a node."""
        return (
            self.db.query(CreditLedger)
            .filter(CreditLedger.node_id == node_id)
            .order_by(CreditLedger.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def reward_task_completion(
        self, 
        node_id: str, 
        task_id: str,
        credits_amount: int
    ) -> CreditLedger:
        """Reward a node for completing a task."""
        return self.add_credits(
            node_id=node_id,
            amount=credits_amount,
            description=f"Task completion reward: {task_id}",
            task_id=task_id,
            transaction_type="earn"
        )
    
    def give_signup_bonus(self, node_id: str, bonus_amount: int = 100) -> CreditLedger:
        """Give a signup bonus to a new node."""
        return self.add_credits(
            node_id=node_id,
            amount=bonus_amount,
            description="Welcome bonus for joining the network",
            transaction_type="bonus"
        )
    
    def get_all_balances(self) -> dict:
        """Get credit balances for all nodes."""
        nodes = self.db.query(Node).all()
        balances = {}
        
        for node in nodes:
            balances[node.id] = {
                "node_name": node.name,
                "balance": self.get_node_balance(node.id),
                "transactions_count": (
                    self.db.query(CreditLedger)
                    .filter(CreditLedger.node_id == node.id)
                    .count()
                )
            }
        
        return balances
