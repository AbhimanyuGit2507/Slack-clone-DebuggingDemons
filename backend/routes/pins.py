from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import User, PinnedMessage, Message, Channel
from ..schemas import PinnedMessageCreate, PinnedMessageSchema
from .auth import get_current_user

router = APIRouter(prefix="/api/pins", tags=["pins"])


@router.post("/channels/{channel_id}/messages/{message_id}", response_model=PinnedMessageSchema)
def pin_message(
    channel_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Pin a message in a channel"""
    # Check if channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if user is member of channel
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    # Check if message exists and belongs to channel
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.channel_id == channel_id
    ).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found in this channel")
    
    # Check if already pinned
    existing_pin = db.query(PinnedMessage).filter(
        PinnedMessage.message_id == message_id,
        PinnedMessage.channel_id == channel_id
    ).first()
    if existing_pin:
        raise HTTPException(status_code=400, detail="Message already pinned")
    
    # Create pin
    pinned_message = PinnedMessage(
        message_id=message_id,
        channel_id=channel_id,
        pinned_by=current_user.id
    )
    db.add(pinned_message)
    db.commit()
    db.refresh(pinned_message)
    
    return pinned_message


@router.get("/channels/{channel_id}", response_model=List[PinnedMessageSchema])
def get_pinned_messages(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all pinned messages in a channel"""
    # Check if channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if user is member of channel
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    pins = db.query(PinnedMessage).filter(
        PinnedMessage.channel_id == channel_id
    ).order_by(PinnedMessage.pinned_at.desc()).all()
    
    return pins


@router.delete("/channels/{channel_id}/messages/{message_id}")
def unpin_message(
    channel_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unpin a message from a channel"""
    # Check if channel exists
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    # Check if user is member of channel
    if current_user not in channel.members:
        raise HTTPException(status_code=403, detail="Not a member of this channel")
    
    # Find the pin
    pin = db.query(PinnedMessage).filter(
        PinnedMessage.message_id == message_id,
        PinnedMessage.channel_id == channel_id
    ).first()
    
    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")
    
    # Only creator or pin creator can unpin
    if channel.created_by != current_user.id and pin.pinned_by != current_user.id:
        raise HTTPException(status_code=403, detail="Only channel creator or pin creator can unpin messages")
    
    db.delete(pin)
    db.commit()
    
    return {"message": "Message unpinned successfully"}
