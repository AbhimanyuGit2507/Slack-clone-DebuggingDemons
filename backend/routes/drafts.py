from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, Draft, Channel
from ..schemas import DraftCreate, DraftUpdate, DraftSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/drafts", tags=["drafts"])


@router.post("/", response_model=DraftSchema)
def save_draft(
    draft_data: DraftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save or update a draft"""
    # Check if draft already exists for this channel/receiver
    existing_draft = db.query(Draft).filter(
        Draft.user_id == current_user.id,
        Draft.channel_id == draft_data.channel_id if draft_data.channel_id else None,
        Draft.receiver_id == draft_data.receiver_id if draft_data.receiver_id else None
    ).first()
    
    if existing_draft:
        # Update existing draft
        existing_draft.content = draft_data.content
        existing_draft.formatting = draft_data.formatting
        existing_draft.mentions = draft_data.mentions
        existing_draft.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_draft)
        return existing_draft
    
    # Create new draft
    draft = Draft(
        user_id=current_user.id,
        channel_id=draft_data.channel_id,
        receiver_id=draft_data.receiver_id,
        content=draft_data.content,
        formatting=draft_data.formatting,
        mentions=draft_data.mentions
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


@router.get("/", response_model=List[DraftSchema])
def get_drafts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all drafts for current user"""
    drafts = db.query(Draft).filter(
        Draft.user_id == current_user.id
    ).order_by(Draft.updated_at.desc()).all()
    return drafts


@router.get("/channel/{channel_id}", response_model=DraftSchema)
def get_channel_draft(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get draft for specific channel"""
    draft = db.query(Draft).filter(
        Draft.user_id == current_user.id,
        Draft.channel_id == channel_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")
    
    return draft


@router.get("/dm/{receiver_id}", response_model=DraftSchema)
def get_dm_draft(
    receiver_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get draft for specific DM conversation"""
    draft = db.query(Draft).filter(
        Draft.user_id == current_user.id,
        Draft.receiver_id == receiver_id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="No draft found")
    
    return draft


@router.put("/{draft_id}", response_model=DraftSchema)
def update_draft(
    draft_id: int,
    draft_update: DraftUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a draft"""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == current_user.id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    if draft_update.content is not None:
        draft.content = draft_update.content
    if draft_update.formatting is not None:
        draft.formatting = draft_update.formatting
    if draft_update.mentions is not None:
        draft.mentions = draft_update.mentions
    
    draft.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(draft)
    return draft


@router.delete("/{draft_id}")
def delete_draft(
    draft_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a draft"""
    draft = db.query(Draft).filter(
        Draft.id == draft_id,
        Draft.user_id == current_user.id
    ).first()
    
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    
    db.delete(draft)
    db.commit()
    return {"message": "Draft deleted successfully"}
