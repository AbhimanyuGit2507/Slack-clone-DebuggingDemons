from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Workflow, Channel
from ..schemas import WorkflowCreate, WorkflowUpdate, WorkflowSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.post("/", response_model=WorkflowSchema)
def create_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new workflow automation"""
    # If channel_id provided, verify membership
    if workflow_data.channel_id:
        channel = db.query(Channel).filter(Channel.id == workflow_data.channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        if current_user not in channel.members:
            raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    workflow = Workflow(
        name=workflow_data.name,
        description=workflow_data.description,
        trigger_type=workflow_data.trigger_type,
        action_type=workflow_data.action_type,
        trigger_config=workflow_data.trigger_config,
        action_config=workflow_data.action_config,
        channel_id=workflow_data.channel_id,
        created_by=current_user.id
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    
    return workflow


@router.get("/", response_model=List[WorkflowSchema])
def list_workflows(
    skip: int = 0,
    limit: int = 50,
    channel_id: int = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all workflows"""
    query = db.query(Workflow).filter(Workflow.created_by == current_user.id)
    
    if channel_id:
        query = query.filter(Workflow.channel_id == channel_id)
    
    if is_active is not None:
        query = query.filter(Workflow.is_active == is_active)
    
    workflows = query.offset(skip).limit(limit).all()
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowSchema)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Only creator can view
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return workflow


@router.put("/{workflow_id}", response_model=WorkflowSchema)
def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Only creator can update
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can update workflow")
    
    if workflow_update.name is not None:
        workflow.name = workflow_update.name
    if workflow_update.description is not None:
        workflow.description = workflow_update.description
    if workflow_update.is_active is not None:
        workflow.is_active = workflow_update.is_active
    
    db.commit()
    db.refresh(workflow)
    
    return workflow


@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Only creator can delete
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can delete workflow")
    
    db.delete(workflow)
    db.commit()
    
    return {"message": "Workflow deleted successfully"}


@router.post("/{workflow_id}/toggle")
def toggle_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle workflow active status"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Only creator can toggle
    if workflow.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can toggle workflow")
    
    workflow.is_active = not workflow.is_active
    db.commit()
    
    return {"message": f"Workflow {'activated' if workflow.is_active else 'deactivated'}"}
