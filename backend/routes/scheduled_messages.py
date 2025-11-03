from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, ScheduledMessage, Channel
from ..schemas import ScheduledMessageCreate, ScheduledMessageUpdate, ScheduledMessageSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/scheduled", tags=["scheduled-messages"])


@router.post("/", response_model=ScheduledMessageSchema)
def schedule_message(
    message_data: ScheduledMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Schedule a message for later"""
    # Validate that scheduled time is in the future
    if message_data.scheduled_for <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
    
    # Validate either channel_id or receiver_id
    if not message_data.channel_id and not message_data.receiver_id:
        raise HTTPException(status_code=400, detail="Must provide either channel_id or receiver_id")
    
    if message_data.channel_id and message_data.receiver_id:
        raise HTTPException(status_code=400, detail="Cannot schedule for both channel and DM")
    
    # If channel, verify membership
    if message_data.channel_id:
        channel = db.query(Channel).filter(Channel.id == message_data.channel_id).first()
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        if current_user not in channel.members:
            raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    # Create scheduled message
    scheduled_msg = ScheduledMessage(
        user_id=current_user.id,
        channel_id=message_data.channel_id,
        receiver_id=message_data.receiver_id,
        content=message_data.content,
        formatting=message_data.formatting,
        mentions=message_data.mentions,
        scheduled_for=message_data.scheduled_for
    )
    db.add(scheduled_msg)
    db.commit()
    db.refresh(scheduled_msg)
    
    return scheduled_msg


@router.get("/", response_model=List[ScheduledMessageSchema])
def get_scheduled_messages(
    status: str = "pending",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all scheduled messages for current user"""
    query = db.query(ScheduledMessage).filter(
        ScheduledMessage.user_id == current_user.id
    )
    
    if status:
        query = query.filter(ScheduledMessage.status == status)
    
    messages = query.order_by(ScheduledMessage.scheduled_for).all()
    return messages


@router.get("/{scheduled_id}", response_model=ScheduledMessageSchema)
def get_scheduled_message(
    scheduled_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific scheduled message"""
    msg = db.query(ScheduledMessage).filter(
        ScheduledMessage.id == scheduled_id,
        ScheduledMessage.user_id == current_user.id
    ).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Scheduled message not found")
    
    return msg


@router.put("/{scheduled_id}", response_model=ScheduledMessageSchema)
def update_scheduled_message(
    scheduled_id: int,
    message_update: ScheduledMessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a scheduled message"""
    msg = db.query(ScheduledMessage).filter(
        ScheduledMessage.id == scheduled_id,
        ScheduledMessage.user_id == current_user.id,
        ScheduledMessage.status == "pending"
    ).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Scheduled message not found or already sent")
    
    if message_update.content is not None:
        msg.content = message_update.content
    if message_update.formatting is not None:
        msg.formatting = message_update.formatting
    if message_update.mentions is not None:
        msg.mentions = message_update.mentions
    if message_update.scheduled_for is not None:
        if message_update.scheduled_for <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
        msg.scheduled_for = message_update.scheduled_for
    
    db.commit()
    db.refresh(msg)
    return msg


@router.delete("/{scheduled_id}")
def cancel_scheduled_message(
    scheduled_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a scheduled message"""
    msg = db.query(ScheduledMessage).filter(
        ScheduledMessage.id == scheduled_id,
        ScheduledMessage.user_id == current_user.id,
        ScheduledMessage.status == "pending"
    ).first()
    
    if not msg:
        raise HTTPException(status_code=404, detail="Scheduled message not found or already sent")
    
    msg.status = "cancelled"
    db.commit()
    
    return {"message": "Scheduled message cancelled"}
